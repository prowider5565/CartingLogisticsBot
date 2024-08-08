from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router

from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.states.auth_state import Registration
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
    await message.answer(greeting)


@command_router.message(Command("/flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    await message.answer("All data has been deleted successfully!")
