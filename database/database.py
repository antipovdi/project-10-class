import asyncio

import aiosqlite
import datetime
import secrets



class DatabaseBot:

    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_file)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.commit()
        await self.db.close()

    async def check_user(self, telegram_id: int) -> bool:
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return user_exist is None

    async def new_user(self, telegram_id: int, contacts: str):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("INSERT INTO users (telegram_id, contacts) VALUES (?, ?)", (telegram_id, contacts, ))

    async def make_object(self, owner: int, title: str, cost: int, start: datetime.datetime, end: datetime.datetime, open_closed: int):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("INSERT INTO objects (owner, title, cost, start, end, code_for_closed) VALUES"
                                     "(?, ?, ?, ?, ?, ?)",
                                     (owner, title, cost, start.strftime('%d/%m/%y-%H:%M'), end.strftime('%d/%m/%y-%H:%M'), (secrets.token_hex(32) if open_closed == 1 else "NULL")))
                return cursor.lastrowid

    async def change_photo(self, obj_id: int, photo: list):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET photos = ? WHERE id = ?", ("NULL" if photo == []  else ';'.join(photo), obj_id,))

    async def add_photo(self, obj_id: int, photo: str):
        async with self.lock:
            async with self.db.execute("SELECT photos FROM objects WHERE id = ?", (obj_id, )) as cursor:
                new_photo = await cursor.fetchone()
                new_photo = new_photo[0]
                if new_photo == "NULL":
                    new_photo = []
                else:
                    new_photo = [new_photo]
                new_photo.append(photo)
                await cursor.execute("UPDATE objects SET photos = ? WHERE id = ?", (';'.join(new_photo), obj_id,))

    async def add_participant(self, obj_id: int, participant_id: int):
        async with self.lock:
            async with self.db.execute("SELECT participants FROM objects WHERE id = ?", (obj_id, )) as cursor:
                new_participants = await cursor.fetchone()
                new_participants = list(new_participants[0])
                new_participants.append(participant_id)
                await cursor.execute("UPDATE objects SET participants = ? WHERE id = ?", (' '.join(new_participants), obj_id,))

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

    async def change_start(self, obj_id: int, start: datetime):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET start = ? WHERE id = ?", (start.strftime('%d/%m/%y-%H:%M'), obj_id,))

    async def change_end(self, obj_id: int, end: datetime):
        async with self.lock:
            async with self.db.cursor() as cursor:
                await cursor.execute("UPDATE objects SET end = ? WHERE id = ?", (end.strftime('%d/%m/%y-%H:%M'), obj_id,))

    async def get_obj(self, obj_id: int) -> dict:
        data = {
            "id": obj_id,
            "title": await self.get_obj_title(obj_id),
            "describe": await self.get_obj_describe(obj_id),
            "start": await self.get_obj_start(obj_id),
            "end": await self.get_obj_end(obj_id),
            "cost": await self.get_obj_cost(obj_id),
            "code": await self.get_obj_code(obj_id),
            "owner": await self.get_obj_owner(obj_id),
            "participants": await self.get_obj_participants(obj_id),
            "photos": await self.get_obj_photo(obj_id)
        }
        return data

    async def get_obj_title(self, obj_id: int) -> str:
        async with self.lock:
            async with self.db.execute("SELECT title FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return res[0]

    async def get_obj_photo(self, obj_id: int) -> list:
        async with self.lock:
            async with self.db.execute("SELECT photos FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                if res[0] is None:
                    return []
                return list(res[0].split(';'))

    async def get_obj_describe(self, obj_id: int) -> str:
        async with self.lock:
            async with self.db.execute("SELECT describe FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                if res[0] is None:
                    return ""
                return res[0]

    async def get_obj_owner(self, obj_id: int) -> int:
        async with self.lock:
            async with self.db.execute("SELECT owner FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return int(res[0])

    async def get_obj_start(self, obj_id: int) -> datetime:
        async with self.lock:
            async with self.db.execute("SELECT start FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return datetime.datetime.strptime(res[0], "%d/%m/%y-%H:%M")

    async def get_obj_end(self, obj_id: int) -> datetime:
        async with self.lock:
            async with self.db.execute("SELECT end FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return datetime.datetime.strptime(res[0], "%d/%m/%y-%H:%M")

    async def get_obj_participants(self, obj_id: int) -> list:
        async with self.lock:
            async with self.db.execute("SELECT participants FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                if res[0] is None:
                    return []
                return list(res[0].split(' '))

    async def get_obj_code(self, obj_id: int) -> str:
        async with self.lock:
            async with self.db.execute("SELECT code_for_closed FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return res[0]

    async def get_obj_cost(self, obj_id: int) -> int:
        async with self.lock:
            async with self.db.execute("SELECT cost FROM objects WHERE id = ?", (obj_id,)) as cursor:
                res = await cursor.fetchone()
                return int(res[0])

    async def get_objs_id_by_owner(self, owner: int) -> list:
        async with self.lock:
            async with self.db.execute("SELECT id FROM objects WHERE owner = ?", (owner,)) as cursor:
                res = await cursor.fetchall()
                if res is None:
                    return []
                return [int(row[0]) for row in res]

