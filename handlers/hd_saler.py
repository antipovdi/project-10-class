from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove
from keyboards.keyboards import get_kb_choose_type, get_kb_adding_photos, get_kb_checking_object
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import LoadNewObj

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("разместить"))
async def new_objects(message: types.Message, state: FSMContext):
    # TODO: создать новое объявление в БД
    await message.answer("Сначала заполним необходимые данные. \n Открытый или закрытый аукцион?", reply_markup=get_kb_choose_type())
    await state.set_state(LoadNewObj.choosing_rent_or_sale)


@router.message(LoadNewObj.choosing_rent_or_sale, F.text.lower().in_(("открытый", "закрытый")))
async def new_object_rent_or_sale(message: types.Message, state: FSMContext, rent_sale: int):
    rent_sale = 1 if F.text.lower() == "открытый" else -1
    await state.set_state(LoadNewObj.checking)
    await new_object_check(message)


async def new_object_check(message: types.Message):
    await message.answer("Так сейчас выглядит твоё объявление:", reply_markup=get_kb_checking_object())
    # TODO: вывод объявления


@router.message(LoadNewObj.checking, F.text.lower().contains("фотографии"))
async def new_object_goto_load_photos(message: types.Message, state: FSMContext):
    await message.answer("Отправь новые фотографии, старые будут удалены", reply_markup=get_kb_adding_photos())
    await state.set_state(LoadNewObj.load_photos)


@router.message(LoadNewObj.checking, F.text.lower().contains("описание"))
async def new_object_goto_add_describe(message: types.Message, state: FSMContext):
    await message.answer("Отправь новое описание, старое будет удалено", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoadNewObj.add_describe)


@router.message(LoadNewObj.checking, F.text.lower().contains("стоимость"))
async def new_object_goto_set_cost(message: types.Message, state: FSMContext):
    await message.answer("Отправь новую стоимость, старая будет удалена", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoadNewObj.add_describe)


@router.message(LoadNewObj.load_photos, F.photo)
async def new_object_load_photos(message: types.Message, state: FSMContext):
    # TODO: сделать сохранение фотографий в БД
    await message.answer(reply_markup=get_kb_adding_photos())
    await state.set_state(LoadNewObj.load_photos)


@router.message(LoadNewObj.load_photos, F.text.lower() == "закончить загрузку фотографий")
async def new_object_stop_load_photos(message: types.Message, state: FSMContext):
    await message.answer("Фотографии обновлены", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoadNewObj.checking)
    await new_object_check(message)


@router.message(LoadNewObj.add_describe, F.text)
async def new_object_add_describe(message: types.Message, state: FSMContext):
    # TODO: добавление описания в БД
    await message.answer("Описание обновлено", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoadNewObj.checking)
    await new_object_check(message)


@router.message(LoadNewObj.set_cost, F.text.regexp(r'[0-9]+'))
async def new_object_set_cost(message: types.Message, state: FSMContext):
    # TODO: добавление стоимости в БД
    await message.answer("Стоимость обновлена")
    await state.set_state(LoadNewObj.checking)
    await new_object_check(message)
