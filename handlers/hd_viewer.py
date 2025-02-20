from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove
from keyboards.kb_home import get_kb_choose_type, get_kb_viewer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import View

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("посмотреть"))
async def show_objects(message: types.Message, state: FSMContext):
    await message.answer("Что тебя интересует? \nАренда или покупка", reply_markup=get_kb_choose_type())
    await state.set_state(View.choosing_rent_or_sale)


@router.message(View.choosing_rent_or_sale, F.text.lower().in_(("аренда", "покупка")))
async def show_objects_rent_or_sale(message: types.Message, state: FSMContext, rent_sale: int):
    rent_sale = 1 if F.text.lower() == "аренда" else -1
    await message.answer("Вот что я могу предложить для аренды:", reply_markup=get_kb_viewer())
    await state.set_state(View.looking)


@router.message(View.looking, F.text.lower() == "дальше")
async def show_objects_next(message: types.Message, state: FSMContext):
    # TODO: добавить показ объявлений
    await message.answer("ОБЯВЛЕНИЕ", reply_markup=get_kb_viewer())


@router.message(View.looking, F.text.lower().contains("избранное"))
async def show_objects_liked(message: types.Message, state: FSMContext):
    # TODO: добавление в избранное
    await message.reply("Добавлено в избранное!", reply_markup=get_kb_viewer())
    show_objects_next()

# TODO: добавить фильтры к обявлениям
