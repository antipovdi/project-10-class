import asyncio
import logging
import aiosqlite
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import hd_cmd, hd_saler, hd_viewer, hd_join
from database.middlewareBD import DatabaseMiddleware
from database.database import DatabaseBot
from handlers.timer import timer

async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Инициализация базы данных
    db_file = "./database/database.db"
    async with aiosqlite.connect(db_file) as con:
        cur = await con.cursor()
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER NOT NULL,
                liked TEXT,
                contacts TEXT NOT NULL,
                PRIMARY KEY(telegram_id)
            )
        """)
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS objects (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                owner INTEGER NOT NULL,
                start TEXT NOT NULL,
                end TEXT NOT NULL,
                cost INTEGER NOT NULL,
                changer INTEGER NOT NULL,
                title TEXT NOT NULL,
                participants TEXT,
                photos TEXT,
                describe TEXT,
                code_for_closed TEXT,
                FOREIGN KEY(owner) REFERENCES users(telegram_id)
            )
        """)
        await con.commit()

    # Инициализация бота и диспетчера
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(hd_cmd.router, hd_viewer.router, hd_saler.router, hd_join.router)
    dp.update.middleware(DatabaseMiddleware(db_file))

    # Запуск таймера как фоновой задачи
    asyncio.create_task(timer(bot, db_file))

    # Запуск поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, rent_sale=0)

if __name__ == "__main__":
    asyncio.run(main())