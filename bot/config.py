from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import logging

from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.handlers.message.auth import auth_router
from bot.roles.general.states.auth_state import Authentication
from .settings import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(auth_router)


@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply(
        f"Xush kelibsiz {message.from_user.full_name}!\nIltimos tilingizni tanlang",
        reply_markup=language_keyboards,
    )
    await state.set_state(Authentication.phone_number)
