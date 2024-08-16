from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.middleware.auth import AuthenticationMiddleware
from bot.utils import query_locale, logger as l
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.utils import get_user


logout_router = Router()
logout_router.message.middleware(AuthenticationMiddleware())


@logout_router.callback_query(lambda query: query.data == "logout")
async def logout_handler(query: types.CallbackQuery, state: FSMContext):
    user = get_user(query.message.chat.id)
    current_lang = query_locale(query.message)
    if user:
        users_collection.update_one(
            {"user_id": query.message.chat.id},
            {"$set": {"credentials.status": "LOGGED_OUT"}},
        )
        await query.message.answer(lang["logout_success"][current_lang])
    else:
        await query.message.answer(
            lang["not_registered"][query.message.from_user.language_code]
        )
