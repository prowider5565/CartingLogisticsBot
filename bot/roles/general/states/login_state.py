from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    password = State()
