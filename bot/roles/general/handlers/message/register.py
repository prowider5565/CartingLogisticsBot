from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from bot.utils import locale, logger as l, silent_delete_message, get_phone_number
from bot.roles.general.keyboards.reply.contact import share_contact_markup
from bot.roles.general.keyboards.inline.user_menu import user_menu_markup
from bot.roles.general.generators.get_scheme import get_context
from bot.roles.general.states.auth_state import Registration
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.settings import settings


register_router = Router()


@register_router.message(Registration.lang)
async def set_language(message: types.Message, state: FSMContext):
    language = {"🇺🇿 O'zbekcha": "uz", "🇷🇺 Русский": "ru", "🇬🇧 English": "en"}
    current_lang = language[message.text]
    await state.update_data(lang=current_lang)
    await message.answer(
        lang["enter_phone_number"][current_lang],
        reply_markup=share_contact_markup(current_lang),
    )
    await state.set_state(Registration.phone_number)


@register_router.message(
    Registration.phone_number, F.content_type.in_({"contact", "text"})
)
async def phone_number_handler(message: types.Message, state: FSMContext):
    phone_number = get_phone_number(message)
    if phone_number is None:
        await message.answer(lang["invalid_phone_number"][await locale(state)])
        await state.set_state(Registration.phone_number)
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
    await state.set_state(Registration.otp)


@register_router.message(Registration.otp)
async def otp_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not message.text.isdigit() and len(message.text) != 4:
        await message.answer(lang["invalid_otp_code"][await locale(state)])
        await state.set_state(Registration.otp)
        return
    response = requests.put(
        f"{settings.DOMAIN}/v1/confirmed_sms?id={data['sms_id']}&sms_code={int(message.text)}"
    )
    l.info(response.json())
    context = response.json()
    if context.get("data", None) is None:
        await message.answer(lang["incorrect_otp_code"][await locale(state)])
        await state.set_state(Registration.otp)
        return

    await message.answer(lang["enter_password"][await locale(state)])
    await state.set_state(Registration.password)


@register_router.message(Registration.password)
async def password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    current_locale = await locale(state)
    await silent_delete_message(message)
    data = await state.get_data()
    response = requests.post(
        f"{settings.DOMAIN}/v1/register_user",
        data={
            "username": data["phone_number"],
            "password": data["password"],
            "id": data["sms_id"],
        },
    )
    await message.answer(
        lang["Registration_succeeded"][current_locale],
        reply_markup=user_menu_markup(current_locale),
    )
    l.info("User credentials are saved to daabase successfully...")
    l.info(response.json())
    users_collection.insert_one(
        get_context(
            message.from_user.id,
            response.json(),
            data["phone_number"],
            data["password"],
            current_locale,
        )
    )
    await state.clear()
