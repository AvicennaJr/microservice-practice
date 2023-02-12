import pytest
from jose import jwt

from app import models, schemas
from app.core.config import settings
from app.core.security import verify_password


def test_user_signup(client):
    resp = client.post(
        "/users/signup",
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


def test_signup_with_existing_email(client, test_user):
    resp = client.post(
        "/users/signup",
        json={
            "email": "hello@gmail.com",
            "password": "somepassword",
            "first_name": "Someone",
            "last_name": "Else",
        },
    )
    assert resp.status_code == 403
    assert resp.json().get("detail") == "Email already in use"


def test_hashed_password(session, test_user):
    user = session.query(models.User).filter(models.User.id == test_user["id"]).first()
    assert verify_password(test_user["password"], user.password)


def test_user_signin(client, test_user):
    resp = client.post(
        "/users/signin",
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


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("hello@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "password1234", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (
            None,
            "password1234",
            422,  # FastAPI return a status code 422 when a schema validation fails
        ),
        ("hello@gmail.com", None, 422),
    ],
)
def test_incorrect_signin(client, email, password, status_code):
    resp = client.post(
        "/users/signin",
        data={"username": email, "password": password},
    )
    assert resp.status_code == status_code


def test_get_user(test_user, authorized_client):
    resp = authorized_client.get("/users/me")
    assert resp.status_code == 200
    user = schemas.UserResponse(**resp.json())
    assert user.id == test_user["id"]
    assert user.first_name == test_user["first_name"]
    assert user.last_name == test_user["last_name"]
    assert user.email == test_user["email"]


def test_update_user(test_user, authorized_client):
    test_user["first_name"] = "new_first_name"
    test_user["last_name"] = "new_last_name"
    test_user["email"] = "new_email@gmail.com"
    resp = authorized_client.put("/users/me", json=test_user)
    assert resp.status_code == 200
    user = schemas.UserResponse(**resp.json())
    assert user.id == test_user["id"]
    assert user.first_name == test_user["first_name"]
    assert user.last_name == test_user["last_name"]
    assert user.email == test_user["email"]


def test_delete_user(authorized_client):
    resp = authorized_client.delete("/users/delete")
    assert resp.status_code == 204
