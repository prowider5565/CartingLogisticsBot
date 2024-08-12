from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from bot.roles.client.states.load import LoadState


load_router = Router()


@load_router.callback_query(lambda query: query.data == "add_load")
async def add_load_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Enter your load Name: ")
    await state.set_state(LoadState.name)
