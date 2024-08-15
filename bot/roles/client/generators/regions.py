from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.constants import regions
from bot.utils import get_user


def get_regions_keyboard(user_id):
    user = get_user(user_id)
    keyboards = []
    region_labels = regions[user["locale"]].keys()

    # Group buttons into rows of 3
    row = []
    for region in region_labels:
        row.append(KeyboardButton(text=region))
        if len(row) == 3:
            keyboards.append(row)
            row = []
    if row:
        keyboards.append(row)  # Add any remaining buttons

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboards, resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard


def get_districts_keyboard(user_id, region):
    user = get_user(user_id)
    keyboards = []
    district_labels = regions[user["locale"]][region]

    # Group buttons into rows of 3
    row = []
    for district in district_labels:
        row.append(KeyboardButton(text=district))
        if len(row) == 3:
            keyboards.append(row)
            row = []
    if row:
        keyboards.append(row)  # Add any remaining buttons

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboards, resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard
