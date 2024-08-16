from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.middleware.auth import AuthenticationMiddleware
from bot.languages.general import lang
from bot.utils import get_user
from bot.languages.general import lang


message_back_router = Router()
message_back_router.message.middleware.register(AuthenticationMiddleware())


@message_back_router.message(
    lambda message: message.text in list(lang["back"].values())
)
async def message_back_handler(message: types.Message, state: FSMContext):
    await state.clear()
    user = get_user(message.chat.id)
    await message.answer(
        lang["warm_greeting"](user["full_name"])[user["locale"]],
        reply_markup=get_user_menu(user["role"]["label"], user["locale"]),
    )
