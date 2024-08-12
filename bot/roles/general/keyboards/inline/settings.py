from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


switch_role_button = InlineKeyboardButton(
    text="Switch Role", callback_data="switch_role"
)
logout_button = InlineKeyboardButton(text="Logout", callback_data="logout")
full_name = InlineKeyboardButton(
    text="Update Fullname", callback_data="update_fullname"
)
settings_markup = InlineKeyboardMarkup(
    inline_keyboard=[[switch_role_button, logout_button, full_name]]
)
