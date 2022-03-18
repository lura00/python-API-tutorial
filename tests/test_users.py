import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schema
from ..app.config import settings
client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello Nyllet ==> BRAINFART'
    assert res.status_code == 200


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def overrid_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user():
    res = client.post(
        "/users/", json={"email": "hello1234@gmail.com", "password": "testpass"})

    # User pydantic models to do some validation
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello1234@gmail.com"
    assert res.status_code == 201
