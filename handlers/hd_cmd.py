from aiogram import F, Router, types
from aiogram.filters.command import Command

from database.database import DatabaseBot
from handlers.my_FSM import Registration
from templates.keyboards import make_kb_from
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

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
        await cmd_home(message, state)


@router.message(Registration.get_contacts)
async def reg_any_other(message: types.Message, state: FSMContext, db: DatabaseBot):
    await db.new_user(message.from_user.id, message.text)
    await message.answer("Спасибо! Вы зарегистрированы.")
    await cmd_home(message, state)


@router.callback_query(F.data == "home")
@router.message(Command("home"))
@router.message(F.text.lower() == "на главную")
async def cmd_home(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Это твоя страница. Что интересует?", reply_markup=make_kb_from(["Посмотреть объявления", "Разместить объявление", "Мои объявления", "Избранное"]))

