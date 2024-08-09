from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.languages.general import lang


user_menu_markup = lambda language: InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=lang["logout"][language], callback_data="logout")]
    ],
)
