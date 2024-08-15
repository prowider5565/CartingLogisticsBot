from aiogram import Router, types

from bot.roles.general.keyboards.inline.settings import get_settings_markup
from bot.languages.general import lang
from bot.utils import get_user


settings_router = Router()


@settings_router.callback_query(lambda query: query.data == "settings")
async def settings_handler(query: types.CallbackQuery):
    user = get_user(query.message.chat.id)
    await query.message.answer(
        lang["select_action"][user["locale"]],
        reply_markup=get_settings_markup(user["locale"], query.message.chat.id),
    )
