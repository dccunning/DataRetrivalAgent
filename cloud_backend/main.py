# API entrypoint (FastAPI)
import os
from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes import login, signup, data_request_history

API_KEY = os.getenv("API_KEY")


def get_api_key(api_key: str = Header(...)):
    """Dependency to check API key."""
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === PUBLIC ROUTES (no auth required) ===
app.include_router(login.router, prefix="/api", tags=["auth"])
app.include_router(signup.router, prefix="/api", tags=["auth"])

# === PROTECTED ROUTES (requires JWT auth) ===
app.include_router(data_request_history.router, prefix="/api", tags=["chats"])


@app.get("/")
def read_root():
    return {"message": "Backend API is running"}
