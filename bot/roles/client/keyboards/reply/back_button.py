from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.languages.client import lang
from bot.utils import get_user


reply_back_button = lambda language: KeyboardButton(
    text=lang["back"][language], callback_data="back_button"
)


def get_reply_back(user_id):
    user = get_user(user_id)
    back_button = KeyboardButton(text=lang["back"][user["locale"]])
    back_button_markup = ReplyKeyboardMarkup(
        keyboard=[[back_button]], resize_keyboard=True, one_time_keyboard=True
    )
    return back_button_markup
