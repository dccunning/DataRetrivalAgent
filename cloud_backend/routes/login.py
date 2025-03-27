import os
import jwt
import bcrypt
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta, timezone
from core.clients.database import Database

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
router = APIRouter()
db = Database()


def create_jwt_token(user):
    """Generate a JWT auth token for the user to call other endpoints in the session."""
    payload = {
        "id": user["id"],
        "email": user["email"],
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/")
def login(data: LoginRequest):
    """Verify the email and password are valid login details and return the auth token."""
    query = "SELECT id, email, password FROM backend.users WHERE email = %s"
    result = db.run_query(query, (data.email,))

    if not result:
        raise HTTPException(status_code=401, detail="Invalid login.")

    user = result[0]
    stored_hash = user["password"].tobytes() if hasattr(user["password"], 'tobytes') else user["password"]

    if not bcrypt.checkpw(data.password.encode("utf-8"), stored_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}
