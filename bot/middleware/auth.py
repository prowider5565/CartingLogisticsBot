from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from bot.roles.general.keyboards.reply.contact import share_contact_markup
from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.states.auth_state import Registration
from bot.roles.general.states.login_state import LoginState
from bot.languages.general import lang
from bot.utils import get_user


logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user = get_user(event.from_user.id)
        state: FSMContext = data["state"]
        if user["status"] == "OK":
            # user is authenticated, proceed with the handler
            return await handler(event, data)
        else:
            if user["status"] == "NOT_REGISTERED":
                # User is not registered at all, brand new user
                await event.answer(
                    f"Xush kelibsiz {event.from_user.full_name}!\nIltimos tilingizni tanlang",
                    reply_markup=language_keyboards,
                )
                await state.set_state(Registration.lang)
            elif user["status"] == "LOGGED_OUT":
                # User is logged out, ask for phone number to log in
                logger.info(user)
                await event.answer(lang["logged_out"][user["locale"]])
                await event.answer(
                    lang["enter_phone_number"][user["locale"]],
                    reply_markup=share_contact_markup(user["locale"]),
                )
                await state.set_state(LoginState.phone_number)

            return