
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from typing import Annotated

from models import User
from db import user_db_worcker, ref_db_worcker
from config import setting
from auth.exceptions import referal_time_expired, referal_not_exist, credentials_exception, access_token_already_expired, user_not_found, invalid_token
from auth.schemes import Token, TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(login: str, password: str):
    user_ = await user_db_worcker.get_user(
        'login', login
    )
    if not user_:
        return False
    if not verify_password(password, user_.password_hash):
        return False
    return user_


def create_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITM)
    return encoded_jwt


def get_jwt(data: dict) -> Token:
    accsess_token = create_token(
        data, expires_delta=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(
        data, expires_delta=setting.REFRESH_TOKEN_EXPIRE_MINUTES)
    token_type = 'bearer'
    return Token(
        access_token=accsess_token,
        refresh_token=refresh_token,
        token_type=token_type
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, setting.SECRET_KEY,
                             algorithms=[setting.ALGORITM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise access_token_already_expired
    user = await user_db_worcker.get_user('login', username)
    if user is None:
        raise user_not_found
    return user


async def republish_tokens(refresh_token: str, login: str):
    user: User = await user_db_worcker.get_user('login', login)
    if user.refresh_token == refresh_token:
        tokens: Token = get_jwt({'sub': login})
        await user_db_worcker.update_user_refreshtoken(login, tokens.refresh_token)
        return tokens
    raise invalid_token


async def get_inform_ref(referal: str = None):
    if referal is not None:
        res = await ref_db_worcker.get_referal('link', referal)
        if res is None:
            raise referal_not_exist
        if res.life_time < datetime.now():
            raise referal_time_expired
        return res
