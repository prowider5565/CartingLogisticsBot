from aiogram import Bot, Dispatcher
import logging

from bot.roles.general.handlers.message.register import register_router
from bot.roles.general.handlers.message.logout import logout_router
from bot.roles.general.handlers.commands import command_router
from .settings import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(register_router)
dp.include_router(logout_router)
dp.include_router(command_router)
