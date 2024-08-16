from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.roles.client.keyboards.reply.back_button import reply_back_button
from bot.languages.keyboards import lang
from bot.utils import get_user


def get_share_location_markup(user_id):
    user = get_user(user_id)
    location_button = KeyboardButton(
        text=lang["share_location"][user["locale"]], request_location=True
    )
    return ReplyKeyboardMarkup(
        keyboard=[[location_button], [reply_back_button(user["locale"])]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
