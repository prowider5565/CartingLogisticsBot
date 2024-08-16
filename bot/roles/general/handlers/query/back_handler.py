from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.middleware.auth import AuthenticationMiddleware
from bot.languages.general import lang
from bot.utils import get_user


back_router = Router()
back_router.message.middleware.register(AuthenticationMiddleware())


@back_router.callback_query(lambda query: query.data == "back_button")
async def back_handler(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["warm_greeting"](user["full_name"])[user["locale"]],
        reply_markup=get_user_menu(user["role"]["label"], user["locale"]),
    )
