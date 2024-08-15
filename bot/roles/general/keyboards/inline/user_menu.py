from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.languages.keyboards import lang


def get_user_menu(role, language):
    markup = [
        InlineKeyboardButton(text=lang["settings"][language], callback_data="settings")
    ]
    match role:
        case "driver":
            pass
        case "client":
            add_load = InlineKeyboardButton(
                text=lang["add_load"][language], callback_data="add_load"
            )
            my_loads = InlineKeyboardButton(
                text=lang["my_loads"][language], callback_data="my_loads"
            )
            markup.append(add_load)
            markup.append(my_loads)
        case "dispatcher":
            pass
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[markup])
    return inline_markup
