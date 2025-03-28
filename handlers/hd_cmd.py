from pyexpat.errors import messages

from aiogram import F, Router, types, Bot
from aiogram.filters import StateFilter
from aiogram.filters.command import Command

from database.database import DatabaseBot
from handlers.my_FSM import Registration
from templates.keyboards import get_kb_home
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup
from handlers.my_FSM import Contact
from templates.text_answer import obj_media_group, obj_text

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, db: DatabaseBot):
    if await db.check_user(message.from_user.id):
        await message.answer(
            "Здравствуйте! \n Это бот для аукционной продажи собственности. \n Для начала, пожалуйста зарегистрируйтесь. " 
            "Укажите предпочитаемые способы связи", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.get_contacts)
    else:
        await message.answer("Здравствуйте! \n Это бот для аукционной продажи собственности. \n Вы уже зарегистрированы! :3")
        await cmd_home(message, state, db)


@router.message(Registration.get_contacts)
async def reg_any_other(message: types.Message, state: FSMContext, db: DatabaseBot):
    await db.new_user(message.from_user.id, message.text)
    await message.answer("Спасибо! Вы зарегистрированы.")
    await cmd_home(message, state, db)


@router.message(Command("home"))
@router.message(F.text.lower() == "на главную")
async def cmd_home(message: types.Message, state: FSMContext, db: DatabaseBot):
    await state.clear()
    contacts = await db.get_user_contacts(message.chat.id)
    await message.answer(f"Контакты: указанные вами: {contacts} \n\n Что интересует?",
                         reply_markup=get_kb_home())


@router.message(StateFilter(None), F.text.lower().contains("контакты"))
async def change_contacts(message: types.Message, state: FSMContext):
    await message.answer("Введите новую информацию")
    await state.set_state(Contact.change)


@router.message(Contact.change)
async def new_contacts(message: types.Message, state: FSMContext, db: DatabaseBot):
    await db.set_user_contacts(message.from_user.id, message.text)
    await cmd_home(message, state, db)


async def show_obj(chat_id: int, obj_id: int, db: DatabaseBot, bot: Bot, kb: InlineKeyboardMarkup|ReplyKeyboardMarkup|ReplyKeyboardRemove) -> types.Message:
    data = await db.get_obj(obj_id)
    if not data['photos'] == []:
        med = (await obj_media_group(data))
        await bot.send_media_group(chat_id=chat_id, media=med)
    txt = await obj_text(data)
    mes = await bot.send_message(chat_id=chat_id, text=txt, reply_markup=kb)
    if not data['code'] is None:
        await bot.send_message(chat_id=chat_id, text=f"Код закрытого аукциона: {data['code']}")
    return mes

