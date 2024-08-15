from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

from bot.languages.keyboards import lang


def get_share_location_markup(language):
    location_button = KeyboardButton(
        text=lang["share_location"][language], request_location=True
    )
    return ReplyKeyboardMarkup(
        keyboard=[[location_button]], resize_keyboard=True, one_time_keyboard=True
    )
