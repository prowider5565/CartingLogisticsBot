from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


location_button = KeyboardButton(text="Share location", request_location=True)
share_location_markup = ReplyKeyboardMarkup(
    keyboard=[[location_button]], resize_keyboard=True, one_time_keyboard=True
)
