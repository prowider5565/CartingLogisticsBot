from aiogram import types, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import logging

from bot.roles.client.handlers.query.add_load import load_router as query_load_router
from bot.roles.general.handlers.message.back_handler import message_back_router
from bot.roles.general.handlers.query.update_credentials import user_router
from bot.roles.client.handlers.query.delete_load import delete_loads_router
from bot.roles.general.handlers.message.register import register_router
from bot.roles.general.handlers.query.settings import settings_router
from bot.roles.general.handlers.query.back_handler import back_router
from bot.roles.general.handlers.query.logout import logout_router
from bot.roles.general.handlers.message.login import login_router
from bot.roles.client.handlers.query.my_loads import loads_router
from bot.roles.driver.handlers.query.load_init import init_router
from bot.roles.general.handlers.commands import command_router
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from .settings import settings
from bot.roles.client.handlers.message.add_load import (
    load_router as message_load_router,
)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
routers = [
    message_load_router,
    delete_loads_router,
    message_back_router,
    query_load_router,
    register_router,
    settings_router,
    command_router,
    logout_router,
    login_router,
    loads_router,
    back_router,
    init_router,
    user_router,
]
dp.include_routers(*routers)


@dp.message(Command("flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    await message.answer("All data has been deleted successfully!")


@dp.message(Command("manual_login"))
async def manual_login_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter phone number")
    await state.set_state(LoginState.phone_number)
