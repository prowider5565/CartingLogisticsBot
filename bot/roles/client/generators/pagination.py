from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.constants import ITEMS_PER_PAGE


def get_loads_markup(loads, current_page):
    keyboards = []
    # Add load buttons
    for i, load in enumerate(loads):
        keyboards.append(
            InlineKeyboardButton(
                text=f"{i + 1}. {load['name']}",
                callback_data=f"load_detail_{current_page}_{i}",
            )
        )

    # Add navigation buttons
    if current_page > 1:
        keyboards.append(
            InlineKeyboardButton(
                text="<< Previous", callback_data=f"my_loads_{current_page - 1}"
            )
        )
    if len(loads) == ITEMS_PER_PAGE:
        keyboards.append(
            InlineKeyboardButton(
                text="Next >>", callback_data=f"my_loads_{current_page + 1}"
            )
        )

    markup = InlineKeyboardMarkup(inline_keyboard=[keyboards], row_width=1)

    return markup
