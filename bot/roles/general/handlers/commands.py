from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router

from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.middleware.auth import AuthenticationMiddleware
from bot.utils import get_user, locale
from bot.languages.general import lang


command_router = Router()
command_router.message.middleware(AuthenticationMiddleware())


@command_router.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    greeting = lang["warm_greeting"](message.from_user.full_name)[
        await locale(message, state)
    ]
    await message.answer(
        greeting, reply_markup=get_user_menu(user["role"]["label"], user["locale"])
    )
