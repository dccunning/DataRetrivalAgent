import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()


def get_db_config():
    return {
        "dbname": os.getenv("DATABASE_NAME"),
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "host": os.getenv("DATABASE_HOST", "localhost"),
        "port": os.getenv("DATABASE_PORT", "5432"),
    }


ENCRYPTION_KEY = os.getenv("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)
