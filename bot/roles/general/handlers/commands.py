from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router

from bot.roles.general.keyboards.inline.user_menu import user_menu_markup
from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.states.login_state import LoginState
from bot.middleware.auth import AuthenticationMiddleware
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.utils import get_user


command_router = Router()
command_router.message.middleware(AuthenticationMiddleware())


@command_router.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    greeting = lang["warm_greeting"](message.from_user.full_name)[user["locale"]]
    await message.answer(greeting, reply_markup=user_menu_markup(user["locale"]))


@command_router.message(Command("/flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    await message.answer("All data has been deleted successfully!")


@command_router.message(Command("manual_login"))
async def manual_login_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter phone number")
    await state.set_state(LoginState.phone_number)
