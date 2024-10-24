from passlib.context import CryptContext
from typing import Dict
from datetime import datetime, timedelta

from referal_api.exeptions import not_availebel_email, not_exist_referal, save_create_error, ttl_error, not_generated_link_error
from db import ref_db_worcker, user_db_worcker
from models import ReferalLink
from referal_api.schemes import UserRefered

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_referal_hash(user: str) -> str:
    return pwd_context.hash(user)


def create_referal_link(referal_head) -> Dict[str, str]:
    return {'referal_link': f'http://127.0.0.1:8000/referal/{referal_head}'}


def get_expire_time(expire: int = 3600):
    expire_time = timedelta(minutes=expire)
    ttl = datetime.now() + expire_time
    return ttl


async def create_and_save_link(user: str, user_id: int) -> bool:
    referal_head = get_referal_hash(user)
    referal_link = create_referal_link(referal_head)
    ttl = get_expire_time()
    result = await ref_db_worcker.set_referal(
        user_id=user_id,
        referal_head=referal_head,
        ttl=ttl
    )
    if not result:
        raise save_create_error

    return referal_link


async def get_referal_head_from_db(login: str) -> str:
    referal_link: ReferalLink = await user_db_worcker.get_refhead_by_filter('login', login)
    if not referal_link:
        raise not_generated_link_error
    return create_referal_link(referal_link)


async def del_referal_link_from_db(user_id: int) -> bool:
    result = await ref_db_worcker.del_referal(user_id)
    if not result:
        raise not_generated_link_error
    return {'status': 'referal deleted'}


async def get_referal_link(referal_head: str = None) -> ReferalLink | bool:
    result: ReferalLink = await ref_db_worcker.get_referal('link', referal_head)
    if not result:
        raise not_exist_referal
    if result.life_time < datetime.now():
        raise not_exist_referal
    return result


async def get_referal_by_email(email: str) -> str | bool:
    ref_link: str = await user_db_worcker.get_refhead_by_filter('email', email)
    if not ref_link:
        raise not_availebel_email
    return create_referal_link(ref_link)


async def get_all_users_refered(id: int):
    all_users = await user_db_worcker.get_all_refered_by_id(id)
    return [UserRefered.from_orm(user) for user in all_users]
