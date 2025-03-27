import bcrypt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend_api.clients.database import Database

router = APIRouter()
db = Database()


class SignupRequest(BaseModel):
    password: str
    email: EmailStr


@router.post("/signup")
def signup(data: SignupRequest):
    """Create a new user with the given email and password."""
    # Check if user already exists
    check_query = "SELECT id FROM users WHERE email = %s"
    existing = db.run_query(check_query, (data.email,))
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_pw = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())

    insert_query = """
        INSERT INTO backend.users (password, email, role)
        VALUES (%s, %s, %s);
    """
    db.run_query(insert_query, (hashed_pw, data.email, "user"))

    return {"message": "Signup successful"}
