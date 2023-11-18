from datetime import datetime

import asyncpg

from config import *


class DB:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )

    # SELECT ===========================================================================================================
    async def user_exists(self, tg: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT tg FROM users WHERE tg = $1', tg
                )
                return False if result is None else True

    async def get_character_greeting(self, character: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT greeting FROM characters WHERE character = $1', character
                )
                return dict(result)['greeting']

    async def get_character_instruction(self, character: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT instruction FROM characters WHERE character = $1', character
                )
                return dict(result)['instruction']

    async def get_character(self, tg: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT character FROM users WHERE tg = $1', tg
                )
                return dict(result)['character']

    # UPDATE ===========================================================================================================
    async def change_character(self, tg: str, character: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'UPDATE users SET character = $1 WHERE tg = $2', character, tg
                )

    # INSERT ===========================================================================================================
    async def create_user(self, tg: str, username: str, name: str, surname: str, time: datetime):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'INSERT INTO users (tg, username, name, surname, time)'
                    'VALUES ($1, $2, $3, $4, $5)',
                    tg, username, name, surname, time
                )

    async def log_message(self, tg: str, message: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'INSERT INTO messages (tg, message)'
                    'VALUES ($1, $2)', tg, message
                )

