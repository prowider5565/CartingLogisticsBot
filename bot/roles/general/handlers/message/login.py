from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.utils import get_user, silent_delete_message, logger as l, get_phone_number
from bot.roles.general.states.login_state import LoginState
from bot.languages.general import lang
from bot.settings import settings


login_router = Router()


@login_router.message(LoginState.phone_number)
async def phone_number_handler(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    phone_number = get_phone_number(message)
    if phone_number is None:
        await message.answer(lang["invalid_phone_number"][user["locale"]])
        await state.set_state(LoginState.phone_number)
        return
    phone_number = phone_number[1:]
    await state.update_data(phone_number=phone_number)
    await message.answer(lang["enter_password"][user["locale"]])
    await state.set_state(LoginState.password)


@login_router.message(LoginState.password)
async def password_handler(message: types.Message, state: FSMContext):
    password = message.text
    data = await state.get_data()
    await silent_delete_message(message)
    url = f"{settings.DOMAIN}/login/user"
    response = requests.post(
        url, data={"username": data["phone_number"], "password": password}
    )
    await message.answer(str(response.json()))
