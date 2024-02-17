from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import os

app = FastAPI()

# Database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

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

@app.post("/signup/")
async def signup(user: User):
    query = "INSERT INTO users(name, senior, interests) VALUES (:name, :senior, :interests)"
    values = {"name": user.name, "senior": user.senior, "interests": user.interests}
    await database.execute(query=query, values=values)
    return {"message": f"User {user.name} signed up successfully!"}

@app.get("/match/")
async def match():
    # Placeholder for matching logic
    # Fetch users from the database and implement matching logic here
    query = "SELECT * FROM users"
    result = await database.fetch_all(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    # Simple example response, adjust according to your matching logic
    return {"message": "Matched users successfully!", "users": result}
