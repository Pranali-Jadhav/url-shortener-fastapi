# Import the FastAPI class from the fastapi package.
# We'll use this class to create our main application object.
from fastapi import FastAPI

# Import the database engine that we created in database.py.
# The engine knows how to connect to our PostgreSQL database.
from database import engine

# Import the Base class from our models.py.
# Base keeps track of all the ORM models (like URL) that inherit from it.
from models import Base
from routers.url import router
# Create a FastAPI application instance.
# 'app' is what Uvicorn will run, and where we will register all our API routes.
app = FastAPI()

# This line tells SQLAlchemy:
# "Look at all the models that inherit from Base, and create the corresponding tables
# in the database if they don't already exist."
# - Base.metadata: holds information about all models/tables
# - .create_all(...): creates the actual tables in PostgreSQL
# - bind=engine: use our PostgreSQL connection for this operation
Base.metadata.create_all(bind=engine)

app.include_router(router)

# This decorator tells FastAPI:
# "When a client sends a GET request to the path '/', call the 'home' function."
@app.get("/")
def home():
    # This function is the handler for GET /
    # Whatever we return here will be converted to JSON and sent as the HTTP response.
    return {"message": "URL Shortener API is working"}
