from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.languages.general import lang


user_menu_markup = InlineKeyboardMarkup(
    keyboard=[
        [InlineKeyboardButton(text=lang["logout"][lang], callback_data="logout")]
    ],
)
