from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# Connecting to your db

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@localhost:5432(port)/fastapi(db-name)'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

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


# TO CONNECT TO DATABASE USING RAW SQL
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database="fastapi", user='postgres',
#                                 password='solstad', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         # import time, this will make the while loop wait 2 secs before starting over.
#         time.sleep(2)
