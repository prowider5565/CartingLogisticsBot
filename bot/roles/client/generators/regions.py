from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


def get_regions_keyboard():
    regions = [
        "Andijan Region",
        "Bukhara Region",
        "Fergana Region",
        "Jizzakh Region",
        "Kashkadarya Region",
        "Khorezm Region",
        "Namangan Region",
        "Navoiy Region",
        "Samarkand Region",
        "Sirdarya Region",
        "Surkhandarya Region",
        "Tashkent Region",
        "Republic of Karakalpakstan",
        "Tashkent City",
    ]
    keyboard = ReplyKeyboardMarkup(row_width=2)
    for region in regions:
        keyboard.add(KeyboardButton(region, callback_data=region))
    return keyboard
