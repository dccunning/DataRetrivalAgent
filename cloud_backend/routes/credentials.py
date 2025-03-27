import json
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from cloud_backend.models.users import User
from core.clients.database import Database
from cloud_backend.utils.auth import get_current_user
from cloud_backend.utils.config import fernet

router = APIRouter()
db = Database()


class CredentialsUpdateRequest(BaseModel):
    credentials: dict


@router.get("/")
def get_credentials(current_user: User = Depends(get_current_user)) -> dict:
    """Fetch and decrypt the credentials JSON blob."""
    query = "SELECT credentials_json FROM backend.users WHERE id = %s"
    result = db.run_query(query, (current_user.id,))

    if not result or not result[0]["credentials_json"]:
        raise HTTPException(status_code=404, detail="No credentials found")

    encrypted_blob = result[0]["credentials_json"]

    try:
        decrypted = fernet.decrypt(encrypted_blob).decode("utf-8")
        return json.loads(decrypted)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to decrypt credentials")


@router.post("/")
def save_credentials(data: CredentialsUpdateRequest, current_user: User = Depends(get_current_user)):
    """Encrypt and store credentials JSON."""
    serialized = json.dumps(data.credentials).encode("utf-8")
    encrypted = fernet.encrypt(serialized)

    query = "UPDATE backend.users SET credentials_json = %s, updated_at = NOW() WHERE id = %s"
    db.run_query(query, (encrypted, current_user.id))

    return {"status": "✅ Credentials saved securely"}
