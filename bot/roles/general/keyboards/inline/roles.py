from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


driver = InlineKeyboardButton(text="Driver", callback_data="driver")
dispatcher = InlineKeyboardButton(text="Dispatcher", callback_data="dispatcher")
client = InlineKeyboardButton(text="Client", callback_data="client")

role_markup = InlineKeyboardMarkup(inline_keyboard=[[driver, dispatcher, client]])
