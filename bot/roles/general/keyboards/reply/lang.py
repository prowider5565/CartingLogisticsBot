from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

langs = [
    KeyboardButton(text="🇺🇿 O'zbekcha"),
    KeyboardButton(text="🇷🇺 Русский"),
    KeyboardButton(text="🇬🇧 English"),
]

language_keyboards = ReplyKeyboardMarkup(keyboard=[langs], resize_keyboard=True)

