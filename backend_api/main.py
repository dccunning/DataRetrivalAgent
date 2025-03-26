# API entrypoint (FastAPI)
from core.clients.database import Database

db = Database(database="data_retrival_agent")
