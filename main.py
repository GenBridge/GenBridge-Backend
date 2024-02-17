from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the User
class User(BaseModel):
    name: str
    email: str
    interests: list[str]

# In-memory storage for demonstration
users = []

@app.post("/signup/")
async def signup(user: User):
    # Here we will add logic to save the user to a database
    users.append(user)
    return {"message": f"User {user.name} signed up successfully!"}

@app.get("/match/")
async def match():
    # Placeholder for matching logic
    # In a real app, we'll fetch users from a database and implement matching logic
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    # Simple example response
    return {"message": "Matched users successfully!"}
