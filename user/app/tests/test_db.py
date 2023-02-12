from app import models


def test_save_to_db(session):

    new_user = models.User(
        email="hello@gmail.com",
        password="password1234",
        first_name="John",
        last_name="Cena",
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    db_user = session.query(models.User).filter(models.User.id == new_user.id).first()

    assert db_user.id == new_user.id
    assert db_user.first_name == new_user.first_name
    assert db_user.last_name == new_user.last_name
    assert db_user.email == new_user.email
    assert db_user.password == new_user.password


def test_read_from_database(test_user, session):
    db_user = (
        session.query(models.User).filter(models.User.id == test_user["id"]).first()
    )

    assert db_user.id == test_user["id"]
    assert db_user.first_name == test_user["first_name"]
    assert db_user.last_name == test_user["last_name"]
    assert db_user.email == test_user["email"]


def test_update_database(test_user, session):

    db_user = (
        session.query(models.User).filter(models.User.id == test_user["id"]).first()
    )

    test_user["email"] = "changing@email.com"

    db_user.email = test_user["email"]
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    edited_user = (
        session.query(models.User).filter(models.User.id == test_user["id"]).first()
    )

    assert edited_user.email == test_user["email"]
