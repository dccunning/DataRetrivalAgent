import logging
import psycopg2
from cloud_backend.utils.config import get_db_config


def run_init_sql():
    db = get_db_config()
    with psycopg2.connect(**db) as conn:
        with conn.cursor() as cur:
            with open("cloud_backend/utils/init.sql") as f:
                cur.execute(f.read())
                conn.commit()
    logging.log(logging.INFO, "✅ Database initialized.")
