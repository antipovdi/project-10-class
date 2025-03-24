from aiogram import F, Router, types, Bot
from aiogram.filters.command import Command, CommandObject
from aiogram.types import ReplyKeyboardRemove

from database.database import DatabaseBot
from aiogram.fsm.context import FSMContext

from handlers.hd_cmd import show_obj
from handlers.hd_cmd import cmd_home
from handlers.my_FSM import View, Join
from templates.keyboards import get_kb_participant
from templates.text_answer import obj_text

router = Router()

@router.message(Command("join"))
async def join_to_close(message: types.Message, command: CommandObject, state: FSMContext, db: DatabaseBot, bot: Bot):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы", reply_markup=ReplyKeyboardRemove())
        return
    code = command.args
    obj_id = await db.get_id_of_closed(code)
    if obj_id is None:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/join <code>")
        return
    await state.set_state(View.looking)
    await state.set_data({'obj_ids': [obj_id]})
    await show_objects_join(message, state, db, bot)


@router.message(View.looking, F.text.lower().contains("участвовать"))
async def show_objects_join(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    mes = await show_obj(message.chat.id, data["obj_ids"][0], db, bot, get_kb_participant())
    await state.update_data(mes=mes)
    await state.set_state(Join.join)

@router.callback_query(F.data == "quit")
async def update_object(callback_query: types.CallbackQuery, state: FSMContext, db: DatabaseBot):
    await cmd_home(callback_query.message, state, db)
    await callback_query.answer()


@router.callback_query(F.data == "update")
async def update_object(callback_query: types.CallbackQuery, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    obj_id = data["obj_ids"][0]
    chat_id = data['mes'].chat.id
    mes_id = data['mes'].message_id
    data = await db.get_obj(obj_id)
    txt = await obj_text(data)
    # await callback_query.message.edit_text(text=txt)
    await bot.edit_message_text(text=txt, chat_id=chat_id, message_id=mes_id)
    await bot.edit_message_reply_markup(reply_markup=get_kb_participant(), chat_id=chat_id, message_id=mes_id)


@router.message(Join.join, F.text.regexp(r'\d+'))
async def joining(message: types.Message, state: FSMContext, db: DatabaseBot):
    data = await state.get_data()
    cost = await db.get_obj_cost(data["obj_ids"][0])
    if cost < int(message.text):
        await db.change_cost(data["obj_ids"][0], int(message.text), message.from_user.id)
