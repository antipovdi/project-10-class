from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def make_kb_from(args) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for txt in args:
        kb.button(text=txt)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_sale() -> ReplyKeyboardMarkup:
    return make_kb_from(["Покупка", "Продажа", "На главную"])

def get_kb_home() -> ReplyKeyboardMarkup:
    return make_kb_from(["Посмотреть объявления", "Разместить объявление", "Мои объявления", "Избранное", "Изменить контакты"])

def get_kb_viewer() -> ReplyKeyboardMarkup:
    return make_kb_from(["Дальше", "Участвовать в аукционе", "Добавить в избранное", "На главную"])

def get_kb_my_viewer() -> ReplyKeyboardMarkup:
    return make_kb_from(["Дальше", "Изменить", "Добавить в избранное", "На главную"])

def get_kb_like_viewer() -> ReplyKeyboardMarkup:
    return make_kb_from(["Дальше", "Участвовать в аукционе", "Удалить из избранного", "На главную"])

def get_kb_participant() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Выйти", callback_data="quit"))
    kb.add(InlineKeyboardButton(text="обновить", callback_data="update"))
    kb.adjust(2)
    return kb.as_markup()


def get_kb_choose_type() -> ReplyKeyboardMarkup:
    return make_kb_from(["Открытый", "Закрытый", "На главную"])


def get_kb_adding_photos() -> ReplyKeyboardMarkup:
    return make_kb_from(["Закончить загрузку фотографий"])


def get_kb_checking_object() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Изменить фотографии", callback_data="photos"))
    kb.add(InlineKeyboardButton(text="Изменить описание", callback_data="describe"))
    kb.add(InlineKeyboardButton(text="Изменить стартовую стоимость", callback_data="cost"))
    kb.add(InlineKeyboardButton(text="Изменить название", callback_data="title"))
    kb.add(InlineKeyboardButton(text="Изменить время", callback_data="time"))
    kb.add(InlineKeyboardButton(text="На главную", callback_data="home"))
    kb.adjust(2, 2, 2)
    return kb.as_markup()


def get_kb_refuse() -> ReplyKeyboardMarkup:
    return make_kb_from(["Отменить"])


def get_kb_join() -> ReplyKeyboardMarkup:
    return make_kb_from(["Указать ставку", "На главную"])
