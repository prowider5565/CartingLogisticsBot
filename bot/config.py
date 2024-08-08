from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import logging

from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.handlers.message.register import register_router

# from bot.roles.general.handlers.message.login import register_router
from bot.roles.general.states.auth_state import Authentication
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.utils import logger as l
from bot.utils import get_user
from .settings import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(register_router)


@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    l.info(user)
    if user:
        greeting = lang["warm_greeting"](message.from_user.full_name)[user["locale"]]
        await message.answer(greeting)
    else:
        await message.reply(
            f"Xush kelibsiz {message.from_user.full_name}!\nIltimos tilingizni tanlang",
            reply_markup=language_keyboards,
        )
        await state.set_state(Authentication.lang)


@dp.message(Command("/flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    await message.answer("All data has been deleted successfully!")
