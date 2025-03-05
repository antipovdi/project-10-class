from aiogram.fsm.state import StatesGroup, State


class LoadNewObj(StatesGroup):
    choosing_rent_or_sale = State()
    checking = State()
    change = State()
    load_photos = State()
    add_describe = State()
    set_cost = State()


class View(StatesGroup):
    looking = State()


class Registration(StatesGroup):
    get_contacts = State()
