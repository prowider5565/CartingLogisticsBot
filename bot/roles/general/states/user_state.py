from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    fullname = State()
    lang = State()
