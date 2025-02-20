from aiogram import F, Router, types
from aiogram.filters.command import Command
from keyboards.kb_home import get_kb_home, get_kb_start, get_kb_rent, get_kb_sale
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, rent_sale: int):
    rent_sale = 0
    await state.clear()
    await message.answer(
        "Привет! \n Это бот для продажи/аренды собственности. \n Что тебя интересует разместить или просмотреть?"
        "объявления?",
        reply_markup=get_kb_start())


@router.message(Command("home"))
@router.message(F.text.lower() == "на главную")
async def cmd_home(message: types.Message, state: FSMContext, rent_sale: int):
    rent_sale = 0
    if state.get_state is not None:
        # TODO: удалить незаконченное объявление из БД
        pass
    await state.clear()
    await message.answer("Это твоя страница. Что интересует?", reply_markup=get_kb_home())

# TODO: сделать показ объявлений пользователя
