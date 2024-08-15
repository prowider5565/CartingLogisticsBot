from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.constants import regions
from bot.utils import get_user


def get_regions_keyboard(user_id):
    user = get_user(user_id)
    keyboards = []
    region_labels = regions[user["locale"]].keys()
    for region in region_labels:
        keyboards.append(KeyboardButton(text=region))
    keyboard = ReplyKeyboardMarkup(
        keyboard=[keyboards], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard


def get_districts_keyboard(user_id, region):
    user = get_user(user_id)
    keyboards = []
    region_labels = regions[user["locale"]][region]
    for region in region_labels:
        keyboards.append(KeyboardButton(text=region))
    keyboard = ReplyKeyboardMarkup(
        keyboard=[keyboards], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard
