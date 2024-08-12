from aiogram import types, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import logging

from bot.roles.general.handlers.query.update_credentials import user_router
from bot.roles.general.handlers.message.register import register_router
from bot.roles.general.handlers.query.settings import settings_router
from bot.roles.client.handlers.message.add_load import (
    load_router as message_load_router,
)
from bot.roles.client.handlers.query.add_load import load_router as query_load_router
from bot.roles.general.handlers.query.switch_role import role_router
from bot.roles.general.handlers.query.logout import logout_router
from bot.roles.general.handlers.message.login import login_router
from bot.roles.general.handlers.commands import command_router
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from bot.utils import logger as l
from .settings import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(message_load_router)
dp.include_router(query_load_router)
dp.include_router(register_router)
dp.include_router(settings_router)
dp.include_router(command_router)
dp.include_router(logout_router)
dp.include_router(login_router)
dp.include_router(user_router)
dp.include_router(role_router)


@dp.message(Command("flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    l.info(list(users_collection.find({})))
    await message.answer("All data has been deleted successfully!")


@dp.message(Command("manual_login"))
async def manual_login_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter phone number")
    await state.set_state(LoginState.phone_number)
