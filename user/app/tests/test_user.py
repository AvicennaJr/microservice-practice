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
        "/users/signin/",
        data={"username": email, "password": password},
    )

    assert resp.status_code == status_code
