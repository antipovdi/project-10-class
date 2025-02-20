from aiogram.fsm.state import StatesGroup, State


class LoadNewObj(StatesGroup):
    choosing_rent_or_sale = State()
    load_photos = State()
    add_discribe = State()
    set_cost = State()
    cheking = State()


class View(StatesGroup):
    choosing_rent_or_sale = State()
    looking = State()
