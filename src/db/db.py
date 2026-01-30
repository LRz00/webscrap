from sqlalchemy import create_engine, text
import os

database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url)
