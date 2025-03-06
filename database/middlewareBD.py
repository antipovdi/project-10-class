from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.database import DatabaseBot


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_file: str) -> None:
        self.db = DatabaseBot(db_file)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        async with self.db as db:
            data['db'] = db
            return await handler(event, data)
