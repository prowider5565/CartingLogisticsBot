from aiogram import Router, types

from bot.roles.general.keyboards.inline.settings import settings_markup


settings_router = Router()


@settings_router.callback_query(lambda query: query.data == "settings")
async def settings_handler(query: types.CallbackQuery):
    await query.message.answer(
        "Select what you wanna do!", reply_markup=settings_markup
    )
