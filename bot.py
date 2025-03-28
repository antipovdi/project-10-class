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
    db_file = "./database/database.db"
    con = await aiosqlite.connect(db_file)
    cur = await con.cursor()
    await cur.execute("CREATE TABLE IF NOT EXISTS \"users\" ("
                    "\"telegram_id\"	INTEGER NOT NULL,"
                    "\"liked\"      TEXT,"    
                    "\"contacts\"	TEXT NOT NULL,"
                    "PRIMARY KEY(\"telegram_id\")"
                    ")")
    await cur.execute("CREATE TABLE IF NOT EXISTS \"objects\" ("
                    "\"id\"	INTEGER NOT NULL,"
                    "\"owner\"	INTEGER NOT NULL,"
                    "\"start\"	TEXT NOT NULL,"
                    "\"end\"	TEXT NOT NULL,"
                    "\"cost\"	INTEGER NOT NULL,"
                    "\"changer\"	INTEGER NOT NULL,"
                    "\"title\"  TEXT NOT NULL,"
                    "\"participants\"	TEXT,"
                    "\"photos\"	TEXT,"
                    "\"describe\"	TEXT,"
                    "\"code_for_closed\" TEXT UNIQUE,"
                    "PRIMARY KEY(\"id\" AUTOINCREMENT),"
                    "FOREIGN KEY(\"owner\") REFERENCES \"users\"(\"telegram_id\")"
                    ")")
    await con.commit()
    await con.close()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=config.bot_token.get_secret_value())
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(hd_cmd.router, hd_viewer.router, hd_saler.router, hd_join.router)
    dp.update.middleware(DatabaseMiddleware(db_file))
    # Запуск процесса поллинга новых апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           rent_sale=0)
    async with DatabaseBot(db_file) as db:
        await timer(bot, db)


if __name__ == "__main__":
    asyncio.run(main())
