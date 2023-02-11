from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True  # allow model to read data even if it's not a dict


class UserSignin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
