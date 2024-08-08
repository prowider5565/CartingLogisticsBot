from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.middleware.auth import AuthenticationMiddleware
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.utils import get_user
from bot.utils import locale


logout_router = Router()
logout_router.message.middleware(AuthenticationMiddleware())


@logout_router.callback_query(lambda query: query.data == "logout")
async def logout_handler(query: types.CallbackQuery, state: FSMContext):
    user = get_user(query.message.from_user.id)
    if user:
        await users_collection.delete_one({"_id": user["_id"]})
        await query.message.answer(lang["logout_success"][await locale(user["locale"])])
    else:
        await query.message.answer(lang["not_registered"][await locale(user["locale"])])
