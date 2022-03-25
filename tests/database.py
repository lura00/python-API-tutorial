import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schema
from app.config import settings
from app.database import get_db, Base


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:solstad@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    # sqlAlchemy create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# When passes client fixture to a test it will start by calling "session" and run the code in session-fixture
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# If use of alembic:
# from alembic import command
# command.upgrade("head")
# command.downgrade("base")

# By using a session fixture as well we can access the db-object and make queries as well as access the client-object in test-functions.
