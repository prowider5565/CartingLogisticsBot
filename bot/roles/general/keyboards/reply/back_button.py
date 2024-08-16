from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from bot.languages.general import lang


def get_reply_back(language):
    back_button = KeyboardButton(text=lang["back"][language])
    back_button_markup = ReplyKeyboardMarkup(
        keyboard=[[back_button]], resize_keyboard=True, one_time_keyboard=True
    )
    return back_button_markup


def get_inline_back(language):
    back_button = InlineKeyboardButton(
        text=lang["back"][language], callback_data="back_button"
    )
    back_button_markup = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    return back_button_markup


back_button = lambda language: InlineKeyboardButton(
    text=lang["back"][language], callback_data="back_button"
)
reply_back_button = lambda language: KeyboardButton(text=lang["back"][language])
