from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.roles.general.states.auth_state import Authentication
from bot.languages.general import lang
from bot.settings import settings
from bot.utils import locale, logger as l

auth_router = Router()


@auth_router.message(Authentication.lang)
async def set_language(message: types.Message, state: FSMContext):
    lang = {"🇺🇿 O'zbekcha": "uz", "🇷🇺 Русский": "ru", "🇬🇧 English": "en"}
    await state.update_data(lang=lang[message.text])
    await message.answer(lang["enter_phone_number"][message.text])
    await state.set_state(Authentication.phone_number)


@auth_router.message(Authentication.phone_number)
async def phone_number_handler(message: types.Message, state: FSMContext):
    request_otp = requests.get(
        f"{settings.DOMAIN}/check_phone?username={message.text}"
    )
    l.info(request_otp.text)
    otp_code, sms_id = (
        request_otp.json()["data"]["sms_code"],
        request_otp.json()["data"]["sms_insert"]["id"],
    )
    await state.update_data(phone_number=message.text, otp=otp_code, sms_id=sms_id)
    await message.answer(lang["enter_your_otp_code"][await locale(state)])
    await state.set_state(Authentication.otp)


@auth_router.message(Authentication.otp)
async def otp_handler(message: types.Message, state: FSMContext):
    otp_code = message.text
    data = await state.get_data()
    if otp_code == data["otp"]:
        await message.answer(lang["enter_fullname"][await locale(state)])
        await state.set_state(Authentication.password)
    else:
        await message.answer(lang["incorrect_otp_code"][await locale(state)])
        await state.set_state(Authentication.otp)


@auth_router.message(Authentication.password)
async def password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = state.get_data()
    l.info(data)
    await message.answer(lang["authentication_succeeded"][await locale(state)])
    await state.finish()
