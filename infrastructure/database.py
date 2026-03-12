import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()  

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_MIN_POOL = int(os.getenv("DB_MIN_POOL", 1))
DB_MAX_POOL = int(os.getenv("DB_MAX_POOL", 10))


class DatabasePool:
    _pool = None
    
    @classmethod
    async def create_pool(cls):
        return await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            min_size=DB_MIN_POOL,
            max_size=DB_MAX_POOL,
        )
    

    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            cls._pool = await cls.create_pool()
        return cls._pool
    

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None