from aiogram import F, Router, types, Bot
from aiogram.types import ReplyKeyboardRemove

from database.database import DatabaseBot
from templates.keyboards import get_kb_choose_type, get_kb_adding_photos, get_kb_checking_object, get_kb_refuse
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.my_FSM import LoadNewObj, ChangeObj
from handlers.hd_cmd import cmd_home, show_obj
import re, datetime

router = Router()


@router.message(StateFilter(None), F.text.lower().contains("разместить"))
async def new_objects(message: types.Message, state: FSMContext):
    await message.answer("Сначала заполним необходимые данные. \n Открытый или закрытый аукцион?", reply_markup=get_kb_choose_type())
    await state.set_state(LoadNewObj.choosing_open_or_close)


@router.message(LoadNewObj.choosing_open_or_close, F.text.lower().in_(("открытый", "закрытый")))
async def new_object_open_or_closed(message: types.Message, state: FSMContext):
    await state.update_data(open_close = (1 if message.text == "открытый" else -1))
    await message.answer("Задайте название объявлению", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoadNewObj.title)


@router.message(LoadNewObj.title)
async def new_obj_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Укажите время аукциона \nНачало и конец через пробел, в формате: DD/MM/YY-hh:mm\n "
                         "Пример: 01/01/25-00:00 01/02/25-00:00\n Если укажите только одну дату, то она будет воспринята как конец")
    await state.set_state(LoadNewObj.time)


@router.message(LoadNewObj.time)
async def new_obj_time(message: types.Message, state: FSMContext):
    dt = []
    for i in re.findall(r'\d{2}/\d{2}/\d{2}-\d{2}:\d{2}', message.text):
        try:
            dt.append(datetime.datetime.strptime(i, "%d/%m/%y-%H:%M"))
        except ValueError:
            await message.answer("Дата и время указаны в неверном формате")
            return
    if len(dt) == 0:
        await message.answer("Дата и время указаны в неверном формате")
        return
    elif len(dt) == 1:
        dt.insert(0, datetime.datetime.now())
    if dt[0] >= dt[1]:
        await message.answer("Дата и время не согласованы (начало позже конца)")
        return
    await state.update_data(start=dt[0], end=dt[1])
    await state.set_state(LoadNewObj.cost)
    await message.answer("Теперь введите начальную стоимость")


@router.message(LoadNewObj.cost)
async def new_obj_cost(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if not re.fullmatch(r"\d+", message.text):
        await message.answer("Стоимость должна быть числом")
        return
    data = await state.get_data()
    obj_id = await db.make_object(message.from_user.id, data['title'], int(message.text), data['start'], data['end'], data['open_close'])
    await message.answer("Объявление добавлено, теперь вы можете его скорректировать и добавить информацию")
    await state.set_data({"id": obj_id})
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)


@router.message(ChangeObj.checking)
async def object_check(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    await message.answer("Так сейчас выглядит твоё объявление:")
    data = await state.get_data()
    await show_obj(message.chat.id, data['id'], db, bot, get_kb_checking_object())

@router.callback_query(F.data == "home")
async def goto_home(callback_query: types.CallbackQuery, state:FSMContext, bot: Bot, db: DatabaseBot):
    await bot.answer_callback_query(callback_query.id)
    await cmd_home(callback_query.message, state, db)

@router.callback_query(F.data == "photos")
async def object_goto_load_photos(message: types.Message, state: FSMContext, db: DatabaseBot):
    data = await state.get_data()
    await db.change_photo(data['id'], [])
    await message.answer("Отправь новые фотографии, старые будут удалены", reply_markup=get_kb_adding_photos())
    await state.set_state(ChangeObj.load_photos)


@router.message(ChangeObj.load_photos, F.photo)
async def object_load_photos(message: types.Message, state: FSMContext, db: DatabaseBot):
    data = await state.get_data()
    await db.add_photo(data['id'], message.photo[-1].file_id)
    await message.answer(text="принято", reply_markup=get_kb_adding_photos())
    await state.set_state(ChangeObj.load_photos)


@router.message(ChangeObj.load_photos, F.text.lower() == "закончить загрузку фотографий")
async def object_stop_load_photos(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    await message.answer("Фотографии обновлены", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)


@router.callback_query(F.data == "describe")
async def object_goto_change_describe(message: types.Message, state: FSMContext):
    await message.answer("Отправь новое описание, старое будет удалено", reply_markup=get_kb_refuse())
    await state.set_state(ChangeObj.set_describe)


@router.callback_query(F.data == "cost")
async def object_goto_change_cost(message: types.Message, state: FSMContext):
    await message.answer("Отправь новую стоимость, старая будет удалена", reply_markup=get_kb_refuse())
    await state.set_state(ChangeObj.set_cost)


@router.callback_query(F.data == "title")
async def object_goto_change_describe(message: types.Message, state: FSMContext):
    await message.answer("Отправь новое название, старое будет удалено", reply_markup=get_kb_refuse())
    await state.set_state(ChangeObj.set_title)


@router.callback_query(F.data == "time")
async def object_goto_change_describe(message: types.Message, state: FSMContext):
    await message.answer("Отправь новое время старта и начала", reply_markup=get_kb_refuse())
    await state.set_state(ChangeObj.set_time)


@router.message(ChangeObj.set_time)
async def object_change_time(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if not message.text.lower() == "отменить":
        data = await state.get_data()
        dt = []
        for i in re.findall(r'\d{2}/\d{2}/\d{2}-\d{2}:\d{2}', message.text):
            try:
                dt.append(datetime.datetime.strptime(i, "%d/%m/%y-%H:%M"))
            except ValueError:
                await message.answer("Дата и время указаны в неверном формате")
                return
        if len(dt) == 0:
            await message.answer("Дата и время указаны в неверном формате")
            return
        elif len(dt) == 1:
            dt.insert(0, datetime.datetime.now())
            if dt[1] < datetime.datetime.now():
                await message.answer(text="Нельзя поставить время в прошлом")
                return
        if dt[0] >= dt[1]:
            await message.answer("Дата и время не согласованы (начало позже конца)")
            return
        await db.change_start(data['id'], dt[0])
        await db.change_end(data['id'], dt[1])
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)


@router.message(ChangeObj.set_title, F.text)
async def object_change_title(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if not message.text.lower() == "отменить":
        data = await state.get_data()
        await db.change_title(data['id'], message.text)
        await message.answer("Название обновлено", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)


@router.message(ChangeObj.set_describe, F.text)
async def object_change_describe(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if not message.text.lower() == "отменить":
        data = await state.get_data()
        await db.change_describe(data['id'], message.text)
        await message.answer("Описание обновлено", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)


@router.message(ChangeObj.set_cost)
async def object_change_cost(message: types.Message, state: FSMContext, db: DatabaseBot, bot: Bot):
    if not message.text.lower() == "отменить":
        if not re.fullmatch(r'\d+', message.text):
            await message.answer(text="Стоимость должна быть числом")
            return
        data = await state.get_data()
        await db.change_cost(data['id'], int(message.text), message.from_user.id)
        await message.answer("Стоимость обновлена")
    await state.set_state(ChangeObj.checking)
    await object_check(message, state, db, bot)
