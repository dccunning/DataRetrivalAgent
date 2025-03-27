# API entrypoint (FastAPI)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import login, signup, credentials, dbt_metadata


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === PUBLIC ROUTES (no auth required) ===
app.include_router(login.router, prefix="/login", tags=["auth"])
app.include_router(signup.router, prefix="/signup", tags=["auth"])
app.include_router(credentials.router, prefix="/credentials", tags=["credentials"])
app.include_router(dbt_metadata.router, prefix="/dbt_metadata", tags=["metadata"])

# === PROTECTED ROUTES (requires JWT auth) ===
# app.include_router(data_request_history.router, prefix="/data_request_history", tags=["requests"])


@app.get("/")
def read_root():
    return {"message": "Backend API is running"}
