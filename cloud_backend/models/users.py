from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    __create_table__ = """
    CREATE TABLE IF NOT EXISTS backend.users (
        id SERIAL PRIMARY KEY,
        password BYTEA NOT NULL,
        email TEXT UNIQUE,
        role TEXT NOT NULL DEFAULT 'user',
        credentials_json BYTEA,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    id: int
    password: bytes
    email: Optional[str] = None
    role: str = "user"
    credentials_json: Optional[bytes] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
