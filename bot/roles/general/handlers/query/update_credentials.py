from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.roles.general.states.user_state import UserState
from bot.utils import get_user, logger as l
from bot.settings import settings


user_router = Router()


@user_router.callback_query(lambda query: query.data == "update_fullname")
async def update_fullname_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Enter your full name")
    await state.set_state(UserState.fullname)


@user_router.message(UserState.fullname)
async def fullname_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    user = get_user(message.from_user.id)
    url = f"{settings.DOMAIN}/v1/update/regis/data"
    data = {
        "username": user["phone_number"],   
        "fullName": message.text,
        "roles": [user["role"]["id"]],
    }
    l.info(data)
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    request = requests.post(url=url, json=data, headers=headers)
    await message.answer(str(request.json()))
