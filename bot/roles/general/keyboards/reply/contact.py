from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from bot.languages.general import lang


share_contact_markup = lambda language: ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text=lang["share_contact"][language], request_contact=True),
        ]
    ],
)
