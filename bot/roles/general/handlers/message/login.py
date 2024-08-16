from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.utils import get_user, silent_delete_message, logger as l, locale
from bot.roles.general.generators.get_scheme import get_context
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.settings import settings


login_router = Router()


@login_router.message(LoginState.password)
async def password_handler(message: types.Message, state: FSMContext):
    password = message.text
    user = get_user(message.from_user.id)
    if user["status"] != "NOT_REGISTERED":
        phone_number = user["phone_number"]
    else:
        data = await state.get_data()
        phone_number = data["phone_number"]
    await silent_delete_message(message)
    url = f"{settings.DOMAIN}/login/user"
    response = requests.post(url, data={"username": phone_number, "password": password})
    if response.status_code == 200:
        if user["status"] == "LOGGED_OUT":
            users_collection.update_one(
                {"user_id": message.from_user.id},
                {
                    "$set": {
                        "credentials.status": "OK",
                        "credentials.token": response.json()["data"]["data"],
                    }
                },
            )
        else:
            users_collection.insert_one(
                get_context(
                    message.from_user.id,
                    response.json()["data"]["data"],
                    phone_number,
                    password,
                    await locale(message, state),
                    message.from_user.full_name,
                )
            )
        accessed_user = get_user(message.from_user.id)
        await message.answer(
            lang["warm_greeting"](accessed_user["full_name"])[accessed_user["locale"]],
            reply_markup=get_user_menu(
                accessed_user["role"]["label"], accessed_user["locale"]
            ),
        )
    else:
        await message.answer(lang["wrong_password"][await locale(message, state)])
        await state.set_state(LoginState.password)
