import asyncio
import aiosqlite
import datetime

from aiogram import types


class DatabaseBot:

    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_file)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    async def check_user(self, telegram_id: int):
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return bool(user_exist)

    async def make_object(self, owner: int, title: str, photo: str, describe: str, cost: int,
                          deadline: datetime.datetime):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("INSERT INTO objects (owner, title, photo, describe, cost, deadline) VALUES"
                                     "(?, ?, ?, ?, ?, ?)",
                                     (owner, title, photo, describe, cost, deadline,))

    async def change_photo(self, obj_id: int, photo: str):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET photo = ? WHERE id = ?", (photo, obj_id,))

    async def change_describe(self, obj_id: int, describe: str):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET describe = ? WHERE id = ?", (describe, obj_id,))

    async def change_cost(self, obj_id: int, cost: int):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET cost = ? WHERE id = ?", (cost, obj_id,))

    async def change_title(self, obj_id: int, title: str):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET title = ? WHERE id = ?", (title, obj_id,))

    async def get_obj(self, obj_id: int):
        async with self.lock:
            async with self.db.execute("SELECT * FROM objects WHERE id = ?", (obj_id,)) as cursor:
                return await cursor.fetchall()

    async def get_objs_by_owner(self, owner: int):
        async with self.lock:
            async with self.db.execute("SELECT id FROM objects WHERE owner = ?", (owner,)) as cursor:
                return await cursor.fetchall()
