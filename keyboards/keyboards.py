from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_kb_from(args) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for txt in args:
        kb.button(text=txt)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_sale() -> ReplyKeyboardMarkup:
    return make_kb_from(["Покупка", "Продажа", "На главную"])


def get_kb_viewer() -> ReplyKeyboardMarkup:
    return make_kb_from(["Дальше", "Участвовать в аукционе", "Добавить в избранное", "На главную"])


def get_kb_choose_type() -> ReplyKeyboardMarkup:
    return make_kb_from(["Открытый", "Закрытый", "На главную"])


def get_kb_adding_photos() -> ReplyKeyboardMarkup:
    return make_kb_from(["Закончить загрузку фотографий"])


def get_kb_checking_object() -> ReplyKeyboardMarkup:
    return make_kb_from(["Изменить фотографии", "Изменить описание", "Изменить стартовую стоимость", "На главную"])


def get_kb_join() -> ReplyKeyboardMarkup:
    return make_kb_from(["Указать ставку", "На главную"])
