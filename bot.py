import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import hd_cmd, hd_saler, hd_viewer
from database.middlewareBD import DatabaseMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=config.bot_token.get_secret_value())
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(hd_cmd.router, hd_viewer.router, hd_saler.router)
    dp.update.middleware(DatabaseMiddleware("database.dp"))
    # Запуск процесса поллинга новых апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           rent_sale=0)
    # rent_sale - переменная, которая опредляет желание пользователя (аренда или покупка)


if __name__ == "__main__":
    asyncio.run(main())
