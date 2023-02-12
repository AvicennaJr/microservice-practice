from pydantic import BaseModel


# Token properties to be sent when a user signs in
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data to expect from the user
class TokenData(BaseModel):
    id: int
