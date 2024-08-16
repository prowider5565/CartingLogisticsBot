from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from bot.roles.general.keyboards.reply.back_button import back_button
from bot.languages.keyboards import lang


def get_role_markup(language):
    role = lang["roles"][language]
    driver = InlineKeyboardButton(text=role[1], callback_data="driver")
    dispatcher = InlineKeyboardButton(text=role[-1], callback_data="dispatcher")
    client = InlineKeyboardButton(text=role[0], callback_data="client")

    return InlineKeyboardMarkup(
        inline_keyboard=[[driver, dispatcher, client], [back_button(language)]]
    )
