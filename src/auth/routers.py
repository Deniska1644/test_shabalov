from fastapi import APIRouter
from fastapi import Depends

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated, Optional

from auth.depends import get_inform_ref, create_token, get_current_user, get_jwt, authenticate_user, get_password_hash, republish_tokens
from models import User
from auth.schemes import UserRegistrSchem, UserLoginSchem, Token
from auth.exceptions import incorrect_username_or_password, user_alredy_exist
from referal_api.schemes import FullReferal
from db import user_db_worcker, transaction_operation

router = APIRouter(
    prefix='/auth'
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise incorrect_username_or_password
    tokens: Token = get_jwt(data={"sub": form_data.username})
    return tokens


@router.post('/registrate')
async def register_user(
    user: UserRegistrSchem,
    referal: Optional[FullReferal] = Depends(get_inform_ref)
):
    hash_password = get_password_hash(user.password)
    tokens: Token = get_jwt(data={'sub': user.login})
    refresh_token = tokens.refresh_token
    if referal is None:
        register_status = await user_db_worcker.register_user(
            login=user.login,
            email=user.email,
            password_hash=hash_password,
            refresh_token=refresh_token
        )
        if register_status:
            return tokens
        raise user_alredy_exist
    register_status = await transaction_operation.registration_user_refer(
        user=user,
        referal=referal,
        hash_password=hash_password,
        refresh_token=refresh_token
    )
    if register_status:
        return tokens
    return {'status': 'hz'}


@router.post('/refresh_token')
async def refresh_token(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)]
):
    refresh_token = current_user.refresh_token
    login = current_user.login
    tokens = await republish_tokens(refresh_token, login)
    return tokens
