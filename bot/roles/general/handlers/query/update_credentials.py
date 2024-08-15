from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.states.user_state import UserState
from bot.nosql.config import users_collection
from bot.utils import get_user, logger as l
from bot.languages.general import lang
from bot.constants import LANGUAGE
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
    l.info(str(list(users_collection.find_one({"user_id": message.from_user.id}))))
    await message.answer(lang["lang_set_successfully"][LANGUAGE[message.text]])
