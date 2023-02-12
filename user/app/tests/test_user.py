from app import schemas

from .database import client, session


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
    # new_user = schemas.UserResponse(**resp.json())
    print(resp.json)
    assert resp.json().get("email") == "hello@gmail.com"
    assert resp.status_code == 201
