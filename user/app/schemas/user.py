from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    """Properties to to expect from a user upon signup"""

    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Properties to send back to the user"""

    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True  # allow model to read data even if it's not a dict


class UserSignin(BaseModel):
    """Properties to expect when a user signs in"""

    email: EmailStr
    password: str


class UserEdit(BaseModel):
    """Properties to expect from a user upon update"""

    first_name: str
    last_name: str
    email: str
    password: Optional[str] = None


class UserInDB(BaseModel):
    """Properties to be stored in the database"""

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
