from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


otp_failed_markup = lambda lang: ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang["resend_otp"][lang]),
            KeyboardButton(text=lang["change_phone_number"][lang]),
        ]
    ]
)
