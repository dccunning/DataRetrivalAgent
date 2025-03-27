from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class DataRequest:
    __create_table__ = """
    CREATE TABLE IF NOT EXISTS backend.data_requests (
        id SERIAL PRIMARY KEY,
        request_text TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('pending', 'success', 'fail')),
        response TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    id: int
    request_text: str
    status: str
    response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
