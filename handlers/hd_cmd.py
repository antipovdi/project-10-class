from aiogram import F, Router, types
from aiogram.filters.command import Command
from handlers.my_FSM import Registration
from keyboards.keyboards import make_kb_from
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # TODO: сделать проверка пользователя зарегистрирован ли он и предложить изменить информацию
    await message.answer(
        "Здравствуйте! \n Это бот для аукционной продажи собственности. \n Для начала, пожалуйста зарегистрируйтесь. " 
        "Укажите предпочитаемые способы связи", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.get_contacts)


@router.message(Registration.get_contacts)
async def reg_any_other(message: types.Message, state: FSMContext):
    # TODO: добавить другое в БД
    await message.answer("Спасибо! Вы зарегистрированы.")
    await cmd_home(message, state)


@router.message(Command("home"))
@router.message(F.text.lower() == "на главную")
async def cmd_home(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Это твоя страница. Что интересует?", reply_markup=make_kb_from(["Посмотреть объявления", "Разместить объявление", "Мои объявления", "Избранное"]))

