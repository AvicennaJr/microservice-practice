from app import schemas


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
