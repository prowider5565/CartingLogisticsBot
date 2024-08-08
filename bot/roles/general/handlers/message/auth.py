from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from bot.roles.general.keyboards.reply.contact import share_contact_markup
from bot.roles.general.states.auth_state import Authentication
from bot.nosql.config import users_collection
from bot.utils import locale, logger as l
from bot.languages.general import lang
from bot.settings import settings

auth_router = Router()


@auth_router.message(Authentication.lang)
async def set_language(message: types.Message, state: FSMContext):
    language = {"🇺🇿 O'zbekcha": "uz", "🇷🇺 Русский": "ru", "🇬🇧 English": "en"}
    current_lang = language[message.text]
    await state.update_data(lang=current_lang)
    await message.answer(
        lang["enter_phone_number"][current_lang],
        reply_markup=share_contact_markup(current_lang),
    )
    await state.set_state(Authentication.phone_number)


@auth_router.message(
    Authentication.phone_number, F.content_type.in_({"contact", "text"})
)
async def phone_number_handler(message: types.Message, state: FSMContext):
    if message.content_type == "text":
        phone_number = message.text
    else:
        phone_number = message.contact.phone_number
    if not (
        phone_number.startswith("+998")
        and phone_number[1:].isdigit()
        and len(phone_number) in range(8, 15)
    ):
        await message.answer(lang["invalid_phone_number"][await locale(state)])
        await state.set_state(Authentication.phone_number)
        return

    request_otp = requests.get(f"{settings.DOMAIN}/check_phone?username={phone_number}")
    if request_otp.json()["data"]["check_phone"]:
        return await message.answer(
            lang["phone_number_already_exists"][await locale(state)]
        )
    otp_code, sms_id = (
        request_otp.json()["data"]["sms_code"],
        request_otp.json()["data"]["sms_insert"]["id"],
    )
    await state.update_data(phone_number=phone_number, sms_id=sms_id)
    await message.answer(
        lang["enter_your_otp_code"][await locale(state)] + str(otp_code)
    )
    await state.set_state(Authentication.otp)


@auth_router.message(Authentication.otp)
async def otp_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not message.text.isdigit() and len(message.text) != 4:
        await message.answer(lang["invalid_otp_code"][await locale(state)])
        await state.set_state(Authentication.otp)
        return
    response = requests.put(
        f"{settings.DOMAIN}/confirmed_sms?id={data['sms_id']}&sms_code={int(message.text)}"
    )
    l.info(response.json())
    context = response.json()
    if context.get("data", None) is None:
        await message.answer(lang["incorrect_otp_code"][await locale(state)])
        await state.set_state(Authentication.otp)
        return

    await message.answer(lang["enter_password"][await locale(state)])
    await state.set_state(Authentication.password)


@auth_router.message(Authentication.password)
async def password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    response = requests.post(
        f"{settings.DOMAIN}/register_user",
        data={
            "username": data["phone_number"],
            "password": data["password"],
            "id": data["sms_id"],
        },
    )
    await message.answer(lang["authentication_succeeded"][await locale(state)])
    await state.clear()
    users_collection.insert_one(
        {"user_id": message.from_user.id, "credentials": response.json()}
    )
