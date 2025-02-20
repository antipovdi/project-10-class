from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# TODO: изменить структуру, сделать maker клавиатур

def get_kb_home() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Посмотреть объявления")
    kb.button(text="Разместить объявление")
    kb.button(text="Мои объявления")
    kb.button(text="Избранное")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Разместить")
    kb.button(text="Посмотреть")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_rent() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Арендодатель")
    kb.button(text="Арендатор")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_sale() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Покупка")
    kb.button(text="Продажа")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_viewer() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Дальше")
    kb.button(text="Добавить в избранное")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_choose_type() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Аренда")
    kb.button(text="Покупка")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_adding_photos() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="закончить загрузку фотографий")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_kb_checking_object() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменить фотографии")
    kb.button(text="Изменить описание")
    kb.button(text="Изменить стоимость")
    kb.button(text="На главную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
