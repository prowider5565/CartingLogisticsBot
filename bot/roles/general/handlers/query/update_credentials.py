from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.roles.general.keyboards.reply.back_button import get_reply_back
from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.keyboards.inline.roles import get_role_markup
from bot.roles.general.states.user_state import UserState
from bot.middleware.auth import AuthenticationMiddleware
from bot.nosql.config import users_collection
from bot.utils import get_user, logger as l
from bot.languages.general import lang
from bot.constants import LANGUAGE
from bot.settings import settings


user_router = Router()
user_router.message.middleware.register(AuthenticationMiddleware())


@user_router.callback_query(lambda query: query.data == "update_fullname")
async def update_fullname_handler(query: types.CallbackQuery, state: FSMContext):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["enter_fullname"][user["locale"]],
        reply_markup=get_reply_back(user["locale"]),
    )
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
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    request = requests.post(url=url, json=data, headers=headers)
    await message.answer(str(request.json()))
    users_collection.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"credentials.full_name": message.text}},
    )


@user_router.callback_query(lambda query: query.data == "change_language")
async def change_language_handler(query: types.CallbackQuery, state: FSMContext):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["choose_language"][user["locale"]], reply_markup=language_keyboards
    )
    await state.set_state(UserState.lang)


@user_router.message(UserState.lang)
async def proceed_language_update_handler(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if message.text not in LANGUAGE.keys():
        await message.answer(lang["invalid_language"][user["locale"]])
        await state.set_state(UserState.lang)
        return
    users_collection.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"credentials.locale": LANGUAGE[message.text]}},
    )
    await message.answer(
        lang["lang_set_successfully"][LANGUAGE[message.text]],
        reply_markup=get_user_menu(role=user["role"]["label"], language=user["locale"]),
    )


@user_router.callback_query(lambda query: query.data == "switch_role")
async def switch_role_handler(query: types.CallbackQuery):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["select_your_role"][user["locale"]],
        reply_markup=get_role_markup(user["locale"]),
    )


@user_router.callback_query(
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
