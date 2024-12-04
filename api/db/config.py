from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_DB = "citus"
POSTGRES_USER = "citus"
POSTGRES_PASSWORD = "z4peRnZYXSFwjkB"
POSTGRES_HOST = "c-vc-board.sdp7gta73xhnts.postgres.cosmos.azure.com"
POSTGRES_PORT = 5432

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)