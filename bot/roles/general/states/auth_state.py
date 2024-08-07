from aiogram.fsm.state import State, StatesGroup


class Authentication(StatesGroup):
    lang = State()
    phone_number = State()
    username = State()
    password = State()
    otp = State()
    sms_id = State()