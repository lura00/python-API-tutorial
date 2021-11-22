from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connecting to your db

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:solstad@localhost/fastapi'

# starting an engine
# If you are connecting to a SQLite db enter this info
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# as well: connect_args={"check_same_thread": False in the ()

# Setting up a session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class

Base = declarative_base()

# dependency
# Creates the request


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
