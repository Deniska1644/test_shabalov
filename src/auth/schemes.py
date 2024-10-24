from pydantic import BaseModel
from pydantic import EmailStr


class UserLoginSchem(BaseModel):
    login: str 
    password: str
    refresh_token: str


class UserRegistrSchem(UserLoginSchem):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
