from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.middleware.auth import AuthenticationMiddleware
from bot.roles.client.states.load import LoadState
from bot.languages.client import lang
from bot.utils import get_user


load_router = Router()
load_router.message.middleware.register(AuthenticationMiddleware())


@load_router.callback_query(lambda query: query.data == "add_load")
async def add_load_handler(query: types.CallbackQuery, state: FSMContext):
    user = get_user(query.message.chat.id)
    await query.message.answer(lang["enter_load_name"][user["locale"]])
    await state.set_state(LoadState.name)
