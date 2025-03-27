import os
import jwt
from jwt import PyJWTError
from fastapi import Header, HTTPException
from cloud_backend.models.user import User

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"


def get_current_user(authorization: str = Header(...)) -> User:
    """Verify and return which user is making the API request.

    :param authorization: Generated JWT key from the user login 'session'
    :return: A user object if it's a valid authorization.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return User(id=payload["id"], email=payload["email"])
