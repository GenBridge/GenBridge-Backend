from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from databases import Database
import os
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

allowed_origins = [
    "http://localhost:3000",  # Assuming your React app runs on localhost:3000
    "https://gen-bridge-frontend.vercel.app/",  # Your production React app domain
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)

# Initialize the Database
database = Database(DATABASE_URL)

# Define a Pydantic model for the User
class User(BaseModel):
    name: str
    senior: bool
    interests: list[str]


# In-memory storage for demonstration
users = []

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Welcome to the GenBridge Backend!"}

@app.post("/signup/")
async def signup(user: User):
    query = "INSERT INTO users(name, senior, interests) VALUES (:name, :senior, :interests)"
    values = {"name": user.name, "senior": user.senior, "interests": user.interests}
    await database.execute(query=query, values=values)
    database.disconnect()
    return {"message": f"User {user.name} signed up successfully!", "match": await match(for_user=user)}

async def match(for_user: User):
    # Fetch users from the database
    match_senior = not for_user.senior
    query = "SELECT * FROM users WHERE senior = :match_senior"
    logger.info("Querying database: %s", query)
    values = {"match_senior": match_senior}
    result = await database.fetch_all(query=query, values=values)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    match = random.choice(result)
    if not match:
        logger.info("No match found")
        return {"message": "No matching users found", "user": match}
    else:
        logger.info("Found match: %s", match)
        return {"message": "Matched users successfully!", "user": match}

