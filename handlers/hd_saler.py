from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove
from keyboards.kb_home import get_kb_choose_type, get_kb_adding_photos, get_kb_checking_object
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import LoadNewObj

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("разместить"))
async def new_objects(message: types.Message, state: FSMContext):
    # TODO: создать новое объявление в БД
    await message.answer("Что тебя интересует? \n Аренда или покупка", reply_markup=get_kb_choose_type())
    await state.set_state(LoadNewObj.choosing_rent_or_sale)


@router.message(LoadNewObj.choosing_rent_or_sale, F.text.lower().in_(("аренда", "покупка")))
async def new_object_rent_or_sale(message: types.Message, state: FSMContext, rent_sale: int):
    rent_sale = 1 if F.text.lower() == "аренда" else -1
    await message.answer("Для начала отправь фотографии", reply_markup=get_kb_adding_photos())
    await state.set_state(LoadNewObj.load_photos)


@router.message(LoadNewObj.load_photos, F.photo)
async def new_object_load_photos(message: types.Message, state: FSMContext):
    # TODO: сделать сохранение фотографий в БД
    await message.answer(reply_markup=get_kb_adding_photos())


@router.message(LoadNewObj.load_photos, F.text.lower() == "закончить загрузку фотографий")
async def new_object_stop_load_photos(message: types.Message, state: FSMContext):
    await message.answer("Добавь описание:")
    await state.set_state(LoadNewObj.add_discribe)


@router.message(LoadNewObj.add_discribe, F.text)
async def new_object_add_describe(message: types.Message, state: FSMContext):
    # TODO: добавление описания в БД
    await message.answer("Укажи стоимость")
    await state.set_state(LoadNewObj.set_cost)


@router.message(LoadNewObj.set_cost, F.text.regexp(r'[0-9]+'))
async def new_object_set_cost(message: types.Message, state: FSMContext):
    # TODO: добавление описания в БД
    await message.answer("Стоимость добавлена")
    await message.answer("Твоё объявление:", reply_markup=get_kb_checking_object())
    await state.set_state(LoadNewObj.cheking)

# TODO: добавить изменение объявлений
