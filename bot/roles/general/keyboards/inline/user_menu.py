from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.languages.general import lang


def user_menu_markup(language):
    switch_role_button = InlineKeyboardButton(
        text="Switch Role", callback_data="switch_role"
    )
    logout_button = InlineKeyboardButton(
        text=lang["logout"][language], callback_data="logout"
    )
    full_name = InlineKeyboardButton(
        text="Update Fullname", callback_data="update_fullname"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[switch_role_button, logout_button, full_name]]
    )
    return markup
