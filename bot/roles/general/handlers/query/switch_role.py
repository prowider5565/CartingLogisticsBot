from aiogram import Router, types
import requests

from bot.roles.general.keyboards.inline.roles import get_role_markup
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.settings import settings
from bot.utils import get_user


role_router = Router()


@role_router.callback_query(lambda query: query.data == "switch_role")
async def switch_role_handler(query: types.CallbackQuery):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["select_your_role"][user["locale"]],
        reply_markup=get_role_markup(user["locale"]),
    )


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
    request = requests.post(url=url, json=data, headers=headers)
    users_collection.update_one(
        {"user_id": query.message.chat.id},
        {"$set": {"credentials.role": {"label": role, "id": roles[role]}}},
    )
    await query.message.answer(str(request.json()))
