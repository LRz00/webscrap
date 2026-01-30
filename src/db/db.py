from sqlalchemy import create_engine, text
import os

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is required but not set")
engine = create_engine(database_url)
