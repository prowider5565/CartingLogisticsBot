from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging

from .settings import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi!")
