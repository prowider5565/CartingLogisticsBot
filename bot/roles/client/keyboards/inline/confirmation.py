from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.languages.client import lang


confirmation_markup = lambda language, load_id: InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=lang["confirm"][language], callback_data=f"codl:{load_id}"
            ),
            InlineKeyboardButton(text=lang["cancel"][language], callback_data=f"cadl"),
        ]
    ]
)
