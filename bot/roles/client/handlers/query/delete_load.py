from aiogram import Router, types
import requests

from bot.roles.client.keyboards.inline.confirmation import confirmation_markup
from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.middleware.auth import AuthenticationMiddleware
from bot.languages.general import lang as general_lang
from bot.languages.client import lang as client_lang
from bot.settings import settings
from bot.utils import get_user


delete_loads_router = Router()
delete_loads_router.message.middleware.register(AuthenticationMiddleware())


@delete_loads_router.callback_query(lambda query: query.data.startswith("delete_load"))
async def delete_load_handler(query: types.CallbackQuery):
    load_id = query.data.split(":")[-1]
    user = get_user(query.message.chat.id)
    await query.message.answer(
        client_lang["are_you_sure"][user["locale"]],
        reply_markup=confirmation_markup(user["locale"], load_id),
    )


@delete_loads_router.callback_query(lambda query: query.data.startswith("codl"))
async def proceed_delete_load_handler(query: types.CallbackQuery):
    load_id = query.data.split(":")[-1]
    user = get_user(query.message.chat.id)
    url = f"{settings.DOMAIN}/loads/delete?id={load_id}"
    headers = {"Authorization": "Bearer {}".format(user["token"]["access_token"])}
    request = requests.delete(url, headers=headers)
    if request.status_code == 200:
        await query.message.answer(
            client_lang["load_deleted"][user["locale"]],
            reply_markup=get_user_menu(user["role"]["label"], user["locale"]),
        )


@delete_loads_router.callback_query(lambda query: query.data.startswith("cadl"))
async def cancel_delete_load_handler(query: types.CallbackQuery):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        general_lang["warm_greeting"](user["full_name"])[user["locale"]],
        reply_markup=get_user_menu(user["role"]["label"], user["locale"]),
    )
