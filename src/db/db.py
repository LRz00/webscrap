from sqlalchemy import create_engine, text
import configs.config as config

database_url = config.database_url
engine = create_engine(database_url)
