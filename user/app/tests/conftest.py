import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import models
from app.api.main import app
from app.core.config import settings
from app.core.security import create_access_token
from app.db import Base, get_db

DATABASE_URL = f"postgresql://{settings.TEST_DATABASE_USERNAME}:{settings.TEST_DATABASE_PASSWORD}@{settings.TEST_DATABASE_HOST}:{settings.TEST_DATABASE_PORT}/{settings.TEST_DATABASE_NAME}"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)  # delete existing test tables
    Base.metadata.create_all(bind=engine)  # create a new table

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        """A helper function to access the test database when required, and close when done"""

        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """Responsible for creating a test user"""

    user_data = {
        "email": "hello@gmail.com",
        "password": "password1234",
        "identification": "123456789",
        "first_name": "John",
        "last_name": "Cena",
    }
    resp = client.post("/users/signup/", json=user_data)
    assert resp.status_code == 201
    new_user = resp.json()
    new_user["password"] = user_data["password"]  # since password isn't in the response
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    """A helper function to access endpoints that require authentication"""

    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client
