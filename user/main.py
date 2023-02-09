from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import oauth
import schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    """A 'post' endpoint to create new users.

    FastAPI will ensure the new user submits the following information (as defined in schemas.UserSignup):
        firstname
        lastname
        email
        password

    It will first check if an email is already in use, and if not it will proceed to create a hash of the
    new user's password and save their information in the database. Otherwise it will return a 403 Forbidden
    error."""

    check_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not check_user:
        hashed_password = oauth.get_password_hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())  # efficiently unpack user details
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email already in use"
        )

    return user


@app.post("/users/signin", response_model=schemas.Token)
def login_for_access_token(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """A 'post' endpoint for users to sign in.

    FastAPI will ensure the user submits the following information:
        email
        password

    It will then first check if a user exists and if a password is valid.
    If both are a valid, it will return a JWT token that will be valid for
    an hour. Otherwise it will return a 404 error."""

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not oauth.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(
    db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)
):
    """A 'get' endpoint to provide information about a user. A user should be authenticated to
    access this endpoint."""

    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    return user


@app.put("/users/me", response_model=schemas.UserResponse)
def update_user(
    updated_details: schemas.UserResponse,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    """A 'put' endpoint to update a user's information.

    FastAPI will ensure the user provides the following information:
        firstname
        lastname
        email

    The user has to be authenticated and they can update any of the fields above."""

    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user.first_name = updated_details.first_name
    user.last_name = updated_details.last_name
    user.email = updated_details.email

    return user


@app.delete("/users/delete ", response_model=schemas.UserResponse)
def update_user(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    """A 'delete' endpoint to delete a user.

    This will permanently delete their account."""

    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
