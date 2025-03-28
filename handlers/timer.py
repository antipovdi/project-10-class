from aiogram import Bot
from aiogram.types import ReplyKeyboardRemove
from database.database import DatabaseBot
from handlers.hd_cmd import show_obj
from asyncio import sleep


async def timer(bot: Bot, db: DatabaseBot):
    while True:
        finished = await db.get_finished()
        if finished:
            for obj_id in finished:
                data = await db.get_obj(obj_id)
                await show_obj(data['changer'], obj_id, db, bot, ReplyKeyboardRemove())
                contacts = await db.get_user_contacts(data['owner'])
                await bot.send_message(chat_id=data['changer'], text=f"Аукцион завершился! Вы победили. Указанные контакты: {contacts}")
                await show_obj(data['owner'], obj_id, db, bot, ReplyKeyboardRemove())
                contacts = await db.get_user_contacts(data['changer'])
                await bot.send_message(chat_id=data['owner'], text=f"Аукцион завершился! Указанные контакты победителя: {contacts}")
                await db.del_obj(obj_id)
        start_soon = await db.get_start_soon()
        if start_soon:
            for obj_id in start_soon:
                data = await db.get_obj(obj_id)
                for p_id in data['participants']:
                    await show_obj(p_id, obj_id, db, bot, ReplyKeyboardRemove())
                    await bot.send_message(chat_id=p_id, text=f"Аукцион скоро начнётся!")
        await sleep(10)
