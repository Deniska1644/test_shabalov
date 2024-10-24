from fastapi import APIRouter, Query
from fastapi import Depends
from typing import Annotated

from auth.schemes import UserRegistrSchem
from models import ReferalLink
from auth.depends import get_current_user
from auth.schemes import UserLoginSchem
from referal_api.depends import get_all_users_refered, create_referal_link, get_referal_by_email, create_and_save_link, get_referal_link, get_referal_head_from_db, get_referal_link, del_referal_link_from_db
from referal_api.schemes import GetReferal, FullReferal, EmailStr
from db import transaction_operation


router = APIRouter(
    prefix='/referal'
)


@router.get('/')
async def get_referal(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)]
):
    ref_link = await get_referal_head_from_db(current_user.login)
    return ref_link


@router.post('/')
async def create_referal(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)]
):
    link = await create_and_save_link(current_user.login, current_user.id)
    return link


@router.delete('/')
async def delete_referal(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)]
):
    res = await del_referal_link_from_db(current_user.id)
    return res


@router.post('/referalemail')
async def get_link_email(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)],
    email: EmailStr,
):
    referal_link = await get_referal_by_email(email)
    return referal_link


@router.post('/referals_by_id')
async def get_all_refered_by_id(
    current_user: Annotated[UserLoginSchem, Depends(get_current_user)],
    id: int = Query(None, ge=1)
):
    a = await get_all_users_refered(id)
    return a
