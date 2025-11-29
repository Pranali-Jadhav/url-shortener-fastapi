from fastapi import HTTPException, APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas import URLCreate
from models import URL
from utils import generate_short_code
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone


router = APIRouter()
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW_MIN = 1

@router.post("/shorten")
def create_short_url(payload: URLCreate, request:Request, db: Session = Depends(get_db)):

    client_ip = request.client.host
    window_start = datetime.now(timezone.utc) - timedelta(minutes=RATE_LIMIT_WINDOW_MIN)

    recent_count = db.query(URL).filter(URL.created_by_ip == client_ip, URL.created_at>=window_start).count()

    if recent_count >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=400,
            detail="Rate limit exceeded. Try again later.")
    existing_url = db.query(URL).filter(URL.original_url==str(payload.original_url)).first()
    if existing_url is not None:
        short_url = f"http://127.0.0.1:8000/{existing_url.short_code}"
        return {"short_url": short_url, "message": "URL already exists, returning existing short URL"}

    code = generate_short_code()

    existing = db.query(URL).filter(URL.short_code==code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Short code collision, try again.")
    
    expires_at = None
    if payload.expires_in_minutes is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=payload.expires_in_minutes)
    url_obj = URL(original_url = str(payload.original_url), short_code=code, expires_at=expires_at, created_by_ip=client_ip)

    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)

    short_url = f"http://127.0.0.1:8000/{code}"

    return {"short_url": short_url}

@router.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):

    url_entry = db.query(URL).filter(URL.short_code==code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="SHort URL not found")
    
    if url_entry.expiry_at is not None :
        now = datetime.now(timezone.utc)
        if now> url_entry.expiry_at:
            raise HTTPException(status_code=410, detail="Short URL has expired")
    url_entry.clicks+=1
    db.commit()

    return RedirectResponse(url=url_entry.original_url)