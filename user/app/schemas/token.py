from pydantic import BaseModel


class Token(BaseModel):
    """Token properties to be sent when a user signs in"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data is the id of the user"""

    id: int
