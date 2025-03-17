from aiogram.fsm.state import StatesGroup, State


class LoadNewObj(StatesGroup):
    choosing_open_or_close = State()
    title = State()
    time = State()
    cost = State()

class ChangeObj(StatesGroup):
    checking = State()
    change = State()
    load_photos = State()
    set_describe = State()
    set_cost = State()
    set_title = State()
    set_time = State()


class View(StatesGroup):
    looking = State()
    join = State()
    set_cost = State()


class Contact(StatesGroup):
    change = State()


class Registration(StatesGroup):
    get_contacts = State()
