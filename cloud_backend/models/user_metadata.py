from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserMetadata:
    __create_table__ = """
    CREATE TABLE IF NOT EXISTS backend.user_metadata (
        user_id INT PRIMARY KEY REFERENCES backend.user(id),
        manifest_json BYTEA,
        catalog_json BYTEA,
        table_summary_json BYTEA,
        table_descriptions_json BYTEA,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    user_id: int
    manifest_json: Optional[bytes] = None
    catalog_json: Optional[bytes] = None
    table_summary_json: Optional[bytes] = None
    table_descriptions_json: Optional[bytes] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
