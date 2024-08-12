from aiogram import Router, types
import requests

from bot.roles.general.keyboards.inline.roles import role_markup
from bot.utils import get_user, logger as l
from bot.settings import settings


role_router = Router()


@role_router.callback_query(lambda query: query.data == "switch_role")
async def switch_role_handler(query: types.CallbackQuery):
    await query.message.answer("Select your role!", reply_markup=role_markup)


@role_router.callback_query(
    lambda query: query.data in ["client", "driver", "dispatcher"]
)
async def process_switch_role_handler(query: types.CallbackQuery):
    role = query.data
    user = get_user(query.message.chat.id)
    url = f"{settings.DOMAIN}/v1/update/regis/data"
    roles = {
        "dispatcher": settings.DISPATCHER,
        "driver": settings.DRIVER,
        "client": settings.CLIENT,
    }
    username = user["phone_number"]
    data = {"roles": [roles[role]], "username": username}
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    l.info("Data: " + str(data))
    request = requests.post(url=url, json=data, headers=headers)
    await query.message.answer(str(request.json()))
