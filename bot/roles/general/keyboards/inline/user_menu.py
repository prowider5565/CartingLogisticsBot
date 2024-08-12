from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_user_menu(role):
    markup = [InlineKeyboardButton(text="Settings", callback_data="settings")]
    match role:
        case "driver":
            pass
        case "client":
            add_load = InlineKeyboardButton(text="Add load", callback_data="add_load")
            markup.append(add_load)
        case "dispatcher":
            pass
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[markup])
    return inline_markup
