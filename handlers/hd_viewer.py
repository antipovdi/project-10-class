from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove
from templates.keyboards import get_kb_viewer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import View

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("посмотреть"))
async def show_objects(message: types.Message, state: FSMContext):
    await message.answer("Вот, что есть на выбор:", reply_markup=get_kb_viewer())
    await state.set_state(View.looking)


@router.message(View.looking, F.text.lower() == "дальше")
async def show_objects_next(message: types.Message, state: FSMContext):
    # TODO: добавить показ объявлений
    await message.answer("ОБЯВЛЕНИЕ", reply_markup=get_kb_viewer())


@router.message(View.looking, F.text.lower().contains("избранное"))
async def show_objects_liked(message: types.Message, state: FSMContext):
    # TODO: добавление в избранное
    await message.reply("Добавлено в избранное!", reply_markup=get_kb_viewer())
    await show_objects_next()


@router.message(View.looking, F.text.lower().contains("участвовать"))
async def show_objects_join(message: types.Message, state: FSMContext):
    # TODO: добавление в избранное
    await message.reply("Информация будет обновляться в реальном времени:", reply_markup=get_kb_viewer())
    await show_objects_next()

# TODO: сделать показ объявлений пользователя
