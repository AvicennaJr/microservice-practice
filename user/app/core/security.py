from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import schemas

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.API_SECRET
ALGORITHM = settings.ALGORITHM
EXPIRY = settings.TOKEN_EXPIRY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")


def verify_password(plain_password, hashed_password):
    """Verify if the user provided password is correct.

    It accepts a plain password and a hashed password and will return
    true if the plain password is correct, otherwise it will return false."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """This will convert a plain password into hashed password"""

    return pwd_context.hash(password)


def create_access_token(data: dict):
    """A function to create bearer tokens.

    This will allow users to access endpoints that require authentication."""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(EXPIRY))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """A function that will verify tokens provided by users.

    It will try to decode the token and return the user's id if
    successful. Otherwise it will return a credentials exception."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """A function to get the user's id from the token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = str(token)

    return verify_access_token(token, credentials_exception)
