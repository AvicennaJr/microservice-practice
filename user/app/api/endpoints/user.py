from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.db.helpers import get_db

router = APIRouter(prefix="/users")


@router.post(
    "/signup",
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
        hashed_password = security.get_password_hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())  # efficiently unpack user details
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email already in use"
        )

    return new_user


@router.post("/signin", response_model=schemas.Token)
def signin(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """A 'post' endpoint for users to sign in.

    FastAPI will ensure the user submits the following information:
        email
        password

    It will first check if a user exists and if a password is valid. If
    both are a valid, it will return a JWT token that will be valid for
    an hour. Otherwise it will return a 403 forbidden error."""

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not security.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = security.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_users_me(
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
) -> None:
    """A 'get' endpoint to provide information about a user. A user should be authenticated to
    access this endpoint."""

    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user


@router.put("/me", response_model=schemas.UserResponse)
def update_user(
    updated_details: schemas.UserEdit,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):
    """A 'put' endpoint to update a user's information.

    FastAPI will ensure the user provides the following information:
        firstname
        lastname
        email

    The user has to be authenticated and they can update any of the fields above."""

    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user.first_name = updated_details.first_name
    user.last_name = updated_details.last_name
    user.email = updated_details.email
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.delete("/delete")
def delete_user(
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):
    """A 'delete' endpoint to delete a user.

    This will permanently delete their account."""

    user = db.query(models.User).filter(models.User.id == current_user.id)
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
