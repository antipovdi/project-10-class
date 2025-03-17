import asyncio

from aiogram import F, Router, types, Bot
from aiogram.types import ReplyKeyboardRemove
from xdg.Locale import regex

from database.database import DatabaseBot
from templates.keyboards import get_kb_viewer, get_kb_participant
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import View
from handlers.hd_cmd import show_obj
from templates.text_answer import obj_media_group, obj_text

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("посмотреть"))
async def show_objects(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    obj_ids = await db.get_open_auctions()
    await state.set_data({"obj_ids": obj_ids})
    await message.answer("Вот, что есть на выбор:", reply_markup=get_kb_viewer())
    await show_obj(message.chat.id, obj_ids[0], db, bot, get_kb_viewer())
    await state.set_state(View.looking)


@router.message(View.looking, F.text.lower() == "дальше")
async def show_objects_next(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    obj_ids = await state.get_data()
    obj_ids = obj_ids["obj_ids"]
    obj_mes = await show_obj(message.chat.id, obj_ids[1], db, bot, get_kb_viewer())
    await state.update_data(obj_ids=obj_ids[1:], obj_mes=obj_mes)


@router.message(View.looking, F.text.lower().contains("избранное"))
async def show_objects_liked(message: types.Message, state: FSMContext, db: DatabaseBot):
    obj_ids = await state.get_data()
    obj_ids = obj_ids["obj_ids"]
    await db.like(message.from_user.id, obj_ids[0])
    await message.reply("Добавлено в избранное!", reply_markup=get_kb_viewer())
    await show_objects_next()


@router.message(View.looking, F.text.lower().contains("участвовать"))
async def show_objects_join(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    obj_ids = await state.get_data()
    obj_ids = obj_ids["obj_ids"]
    await show_obj(message.chat.id, obj_ids[0], db, bot, get_kb_participant())
    await state.set_state(View.join)


@router.callback_query(F.data == "quit")
async def update_object(state: FSMContext):
    await state.set_state(View.looking)


@router.callback_query(F.data == "update")
async def update_object(callback_query: types.CallbackQuery, state: FSMContext, db: DatabaseBot):
    obj_ids = await state.get_data()
    obj_id = obj_ids["obj_ids"][0]
    data = await db.get_obj(obj_id)
    txt = await obj_text(data)
    await callback_query.message.edit_text(txt)



@router.message(View.join, F.text.regexp(r'\d+'))
async def joining(message: types.Message, state: FSMContext, db: DatabaseBot):
    obj_ids = await state.get_data()
    obj_ids = obj_ids["obj_ids"]
    await db.change_cost(obj_ids[1], int(message.text), message.from_user.id)
