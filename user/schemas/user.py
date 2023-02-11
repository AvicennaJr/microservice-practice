from typing import Optional

from pydantic import BaseModel, EmailStr


# Properties to receive when a user signs up
class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


# Properties to send back to the user
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True  # allow model to read data even if it's not a dict


# Properties to receive when a user signs in
class UserSignin(BaseModel):
    email: EmailStr
    password: str


# Properties to receive when a user wants to update
class UserEdit(BaseModel):
    first_name: str
    last_name: str
    email: str


# Properties to be stored in the database
class UserInDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
