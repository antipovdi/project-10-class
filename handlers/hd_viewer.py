from aiogram import F, Router, types, Bot
from handlers.hd_cmd import cmd_home

from database.database import DatabaseBot
from templates.keyboards import get_kb_viewer, get_kb_my_viewer, get_kb_like_viewer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import View, ChangeObj
from handlers.hd_cmd import show_obj
from handlers.hd_saler import object_check

router = Router()

@router.message(StateFilter(None), F.text.lower().in_({"посмотреть объявления", "мои объявления", "избранное"}))
async def look_objects(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if message.text.lower() == "мои объявления":
        obj_ids = await db.get_objs_id_by_owner(message.from_user.id)
        kb = get_kb_my_viewer()
    elif message.text.lower() == "избранное":
        obj_ids = await db.get_liked(message.from_user.id)
        kb = get_kb_like_viewer()
    else:
        obj_ids = await db.get_open_auctions(message.from_user.id)
        kb = get_kb_viewer()
    await state.set_data({'obj_ids': obj_ids, 'kb': kb})
    await state.set_state(View.looking)
    await show_objects(message, state, db, bot)

async def show_objects(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    if len(data['obj_ids']) == 0:
        await message.answer("Нет никаких объявлений")
        await cmd_home(message, state, db)
    else:
        await show_obj(message.chat.id, data['obj_ids'][0], db, bot, data['kb'])
        await state.set_state(View.looking)


@router.message(View.looking, F.text.lower() == "дальше")
async def show_objects_next(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    data['obj_ids'].pop(0)
    await state.update_data(obj_ids=data['obj_ids'])
    await show_objects(message, state, db, bot)


@router.message(View.looking, F.text.lower().contains("избранное"))
async def show_objects_liked(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    await db.like(message.from_user.id, data["obj_ids"][0])
    await message.reply("Добавлено в избранное!", reply_markup=data['kb'])


@router.message(View.looking, F.text.lower().contains("изменить"))
async def change_my_obj(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    data = await state.get_data()
    await state.set_state(ChangeObj.checking)
    await state.set_data({'id': data['obj_ids'][0]})
    await object_check(message, state, db, bot)


@router.message(View.looking, F.text.lower() == "удалить из избранного")
async def show_objects_unliked(message: types.Message, state: FSMContext, db: DatabaseBot):
    data = await state.get_data()
    await db.unlike(message.from_user.id, data["obj_ids"][0])
    await message.reply("Удалено из избранного!", reply_markup=data['kb'])


@router.message(View.looking, F.text.lower() == "удалить")
async def show_objects_unliked(message: types.Message, state: FSMContext, db: DatabaseBot):
    data = await state.get_data()
    await db.del_obj(data["obj_ids"][0])
    await message.reply("Удалено!", reply_markup=data['kb'])
