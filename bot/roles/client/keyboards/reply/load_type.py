from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.roles.client.keyboards.reply.back_button import reply_back_button
from bot.constants import LOAD_TYPES
from bot.utils import get_user


def get_type_markup(user_id):
    user = get_user(user_id)
    keyboards = []
    for text in LOAD_TYPES[user["locale"]]:
        keyboards.append(KeyboardButton(text=text))
    return ReplyKeyboardMarkup(
        keyboard=[keyboards, [reply_back_button(user["locale"])]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
