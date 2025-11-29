# In FastAPI, schemas.py contains Pydantic models, which:
# Validate incoming data
# Ensure the API receives correct JSON
# Define what fields exist in a request
# Convert data to proper Python types

from pydantic import BaseModel, HttpUrl
from typing import Optional
class URLCreate(BaseModel):
    original_url:HttpUrl
    expires_in_minutes: Optional[int] = None