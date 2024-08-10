from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.utils import get_user, silent_delete_message, logger as l, locale
from bot.roles.general.generators.get_scheme import get_context
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.settings import settings


login_router = Router()


# @login_router.message(LoginState.phone_number)
# async def phone_number_handler(message: types.Message, state: FSMContext):
#     user = get_user(message.from_user.id)
#     phone_number = get_phone_number(message)
#     if phone_number is None:
#         # await message.answer(lang["invalid_phone_number"][user["locale"]])
#         await message.answer("Invalid phone number")
#         await state.set_state(LoginState.phone_number)
#         return
#     phone_number = phone_number[1:]
#     await state.update_data(phone_number=phone_number)
#     # await message.answer(lang["enter_password"][user["locale"]])
#     await message.answer("Enter password")
#     await state.set_state(LoginState.password)


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
        l.info("PRINTING PASS")
        l.info(user)
        if user:
            users_collection.update_one(
                {"user_id": message.from_user.id},
                {
                    "$set": {
                        "credentials.status": "OK",
                        "credentials.token": response.json()["data"]["data"],
                    }
                },
            )
            l.info("THE UPDATED USER &&&&&&&&&&&&&&&&&&&")
            l.info(users_collection.find_one({"user_id": message.from_user.id}))
        else:
            l.info("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
            l.info(response.json())
            users_collection.insert_one(
                get_context(
                    message.from_user.id,
                    response.json()["data"]["data"],
                    phone_number,
                    password,
                    locale(message),
                )
            )
        await message.answer(str(response.json()))
    else:
        await message.answer(lang["wrong_password"][locale(message)])
        await state.set_state(LoginState.password)
