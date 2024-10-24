import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from typing import AsyncGenerator

from auth.schemes import UserRegistrSchem
from config import setting
from models import User, ReferalLink, Invited
from auth.exceptions import user_alredy_exist
from redis_cache.redis_worcker import cached_save


class DbWorcker:
    DATABASE_URL = setting.get_pg_dns()

    def __init__(self):
        self.engine = create_async_engine(self.DATABASE_URL)
        self.async_session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)


class UserDBWorcker(DbWorcker):
    async def register_user(self, login: str, email: str, password_hash: str, refresh_token: str) -> bool:
        async with self.async_session_maker() as session:
            try:
                query = insert(User).values(
                    login=login,
                    email=email,
                    password_hash=password_hash,
                    refresh_token=refresh_token
                )
                await session.execute(query)
                await session.commit()
                return True

            except IntegrityError as e:
                print(e)
                return False

    async def get_user(self, filter_field: str, filter_value: int | str) -> User | None:
        async with self.async_session_maker() as session:
            try:
                query = select(User).where(
                    getattr(User, filter_field) == filter_value)
                res = await session.execute(query)
                user = res.scalars().first()
                return user

            except IntegrityError:
                return False

    async def update_user_refreshtoken(self, login: str, refreshtoken: str) -> bool:
        async with self.async_session_maker() as session:
            try:
                query = select(User).where(User.login == login)
                res = await session.execute(query)
                user = res.scalars().first()
                if user:
                    user.refresh_token = refreshtoken
                    await session.commit()
                    return True
                return False

            except IntegrityError:
                return False

    async def get_refhead_by_filter(self, filter_field: str, filter_value: str | int) -> User | None:
        async with self.async_session_maker() as session:
            try:
                query = select(User).where(
                    getattr(User, filter_field) == filter_value)
                res = await session.execute(query)
                user = res.scalars().first()
                if user:
                    query_ = select(ReferalLink).where(
                        ReferalLink.user_id == user.id)
                    res = await session.execute(query_)
                    link = res.scalars().first()
                    if link:
                        return link.link
                    return None
                return None

            except IntegrityError:
                return None

    async def get_all_refered_by_id(self, id) -> User | None:
        async with self.async_session_maker() as session:
            try:
                query = (
                    select(User)
                    .join(Invited, Invited.user_invited_id == User.id)
                    .filter(Invited.user_inviting_id == id)
                )
                res = await session.execute(query)
                users = res.scalars().all()
                return users

            except Exception as e:
                return None


class ReferalDBWorcker(DbWorcker):
    @cached_save()
    async def set_referal(self, user_id: int, referal_head: str, ttl):
        async with self.async_session_maker() as session:
            try:
                query = insert(ReferalLink).values(
                    user_id=user_id,
                    link=referal_head,
                    life_time=ttl,
                    used=False
                )
                await session.execute(query)
                await session.commit()
                return True

            except IntegrityError:
                return False

    async def get_referal(self, filter_field: str, filter_value) -> ReferalLink | bool:
        async with self.async_session_maker() as session:
            try:
                query = select(ReferalLink).where(
                    getattr(ReferalLink, filter_field) == filter_value)
                res = await session.execute(query)
                ref = res.scalars().first()
                return ref
            except IntegrityError:
                return None
            except AttributeError:
                raise ValueError(f"Invalid filter field: {filter_field}")

    async def del_referal(self, user_id: int):
        async with self.async_session_maker() as session:
            try:
                query = delete(ReferalLink).where(
                    ReferalLink.user_id == user_id)
                res = await session.execute(query)
                await session.commit()
                if res.rowcount == 0:
                    return False
                return True

            except IntegrityError:
                return False


class TransactionOperation(DbWorcker):
    async def registration_user_refer(self, user: UserRegistrSchem, referal: ReferalLink, hash_password: str, refresh_token: str):
        async with self.async_session_maker() as session:
            async with session.begin():
                try:
                    query = insert(User).values(
                        login=user.login,
                        email=user.email,
                        password_hash=hash_password,
                        refresh_token=refresh_token
                    ).returning(User.id)
                    res = await session.execute(query)
                    user_registrade = res.fetchone()

                    if user_registrade is None:
                        raise user_alredy_exist

                    query = delete(ReferalLink).where(
                        ReferalLink.link == referal.link)
                    await session.execute(query)

                    query = insert(Invited).values(
                        user_inviting_id=referal.user_id,
                        user_invited_id=user_registrade[0],
                        referal_head=referal.link)
                    await session.execute(query)
                    return True

                except Exception as e:
                    print(f'exeption: {e}')
                    return None


user_db_worcker = UserDBWorcker()
ref_db_worcker = ReferalDBWorcker()
transaction_operation = TransactionOperation()
