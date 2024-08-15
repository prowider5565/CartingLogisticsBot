from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.constants import regions


def get_regions_keyboard():
    keyboards = []
    region_labels = regions.keys()
    for region in region_labels:
        keyboards.append(KeyboardButton(text=region))
    keyboard = ReplyKeyboardMarkup(
        keyboard=[keyboards], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard
