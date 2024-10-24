# from redis.redis_conn import aioredis_get_pool
import asyncio
import redis.asyncio as redis
from functools import wraps


class RedisWorcker:
    def __init__(self):
        self.pool = None

    async def aioredis_get_pool(self) -> None:
        self.pool = redis.Redis(
            host='localhost',
            port='6379',
            decode_responses=True,
        )

    async def set_redis(self, key: str | int, value: str | int) -> None:
        try:
            async with self.pool as conn:
                res = await conn.set(key, value)
                print(res)

        except Exception as e:
            print(e)

    async def get_redis(self, key: str | int):
        try:
            async with self.pool as conn:
                res = await conn.get(key)
                print(res)
                return res

        except Exception as e:
            print(e)

    async def delete_redis(self, key: str | int) -> None:
        try:
            async with self.pool as conn:
                res = await conn.delete(key)
                print(res)

        except Exception as e:
            print(e)


cls = RedisWorcker()


def cached_save():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = kwargs.get('referal_head')
            value = kwargs.get('user_id')
            await cls.aioredis_get_pool()
            res = await cls.get_redis(key)
            if res:
                raise ValueError('уже в кеше')
            await cls.set_redis(key, value)
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# def cached_del():
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             key = kwargs.get('referal_head')
#             await cls.aioredis_get_pool()
#             res = await cls.get_redis(key)
#             if res:
#                 print('уже в кеше')
#             await cls.set_redis(key, value)
#             result = await func(*args, **kwargs)
#             return result
#         return wrapper
#     return decorator



