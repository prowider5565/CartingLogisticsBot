from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.constants import LOAD_TYPES


def get_type_markup(lang):
    keyboards = []
    for text in LOAD_TYPES[lang]:
        keyboards.append(KeyboardButton(text=text))
    return ReplyKeyboardMarkup(
        keyboard=[keyboards], resize_keyboard=True, one_time_keyboard=True
    )
