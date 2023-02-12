import pytest
from jose import jwt

from app import schemas
from app.core.config import settings


def test_user_signup(client):
    resp = client.post(
        "/users/signup/",
        json={
            "email": "hello@gmail.com",
            "password": "password1234",
            "first_name": "John",
            "last_name": "Cena",
        },
    )
    new_user = schemas.UserResponse(**resp.json())
    assert new_user.first_name == "John"
    assert new_user.last_name == "Cena"
    assert new_user.email == "hello@gmail.com"
    assert resp.status_code == 201


def test_user_signin(client, test_user):
    resp = client.post(
        "/users/signin/",
        data={
            "username": test_user["email"],  # fastapi expects username instead of email
            "password": test_user["password"],
        },
    )
    token = schemas.Token(**resp.json())
    payload = jwt.decode(
        token.access_token, settings.API_SECRET, algorithms=[settings.ALGORITHM]
    )
    assert payload.get("user_id") == test_user["id"]
    assert token.token_type == "bearer"
    assert resp.status_code == 200


def test_incorrect_signin(client, test_user):
    resp = client.post(
        "/users/signin/",
        data={"username": test_user["email"], "password": "WrongPassword"},
    )

    assert resp.status_code == 403
    assert resp.json().get("detail") == "Invalid Credentials"
