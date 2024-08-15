from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from bot.languages.keyboards import lang
from bot.utils import get_user


def get_settings_markup(language, user_id):
    user = get_user(user_id)
    switch_role_button = InlineKeyboardButton(
        text=lang["switch_role"](user["role"]["label"])[language],
        callback_data="switch_role",
    )
    logout_button = InlineKeyboardButton(
        text=lang["logout"][language], callback_data="logout"
    )
    full_name = InlineKeyboardButton(
        text=lang["update_fullname"](user["full_name"])[language],
        callback_data="update_fullname",
    )
    change_language_button = InlineKeyboardButton(
        text=lang["change_language"](user["locale"])[language],
        callback_data="change_language",
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [full_name],
            [switch_role_button],
            [change_language_button],
            [logout_button],
        ]
    )
