from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from bot.roles.general.keyboards.reply.back_button import back_button
from bot.languages.client import lang
from bot.utils import get_user


def get_delete_load_button(load_id, user_id):
    user = get_user(user_id)
    button = InlineKeyboardButton(
        text=lang["delete_this_load"][user["locale"]],
        callback_data=f"delete_load:{load_id}",
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button, back_button(user["locale"])]]
    )
    return markup
