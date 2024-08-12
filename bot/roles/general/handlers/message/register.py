from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from bot.utils import locale, logger as l, silent_delete_message, get_phone_number
from bot.roles.general.keyboards.reply.contact import share_contact_markup
from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.roles.general.generators.get_scheme import get_context
from bot.roles.general.states.auth_state import Registration
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.settings import settings


register_router = Router()


@register_router.message(Registration.lang)
async def set_language(message: types.Message, state: FSMContext):
    language = {"🇺🇿 O'zbekcha": "uz", "🇷🇺 Русский": "ru", "🇬🇧 English": "en"}
    current_lang = await locale(message, state)
    if message.text not in language.keys():
        await message.answer(lang["invalid_language"][current_lang])
        await state.set_state(Registration.lang)
        return
    await state.update_data(lang=language[message.text])
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
    phone_number = phone_number[1:]
    current_locale = await locale(message, state)
    if phone_number is None:
        await message.answer(lang["invalid_phone_number"][current_locale])
        await state.set_state(Registration.phone_number)
        return
    l.info("Phone number >>>>>>>>>>>>>>>>>>>>> " + phone_number)
    request_otp = requests.get(
        f"{settings.DOMAIN}/v1/check_phone?username={phone_number}"
    )
    if request_otp.json():
        l.info(request_otp.json())
        if request_otp.json()["data"]["check_phone"]:
            await message.answer(lang["phone_number_already_exists"][current_locale])
            await message.answer(lang["login_instead"][current_locale])
            await state.update_data(phone_number=phone_number)
            await state.set_state(LoginState.password)
            return
    otp_code, sms_id = (
        request_otp.json()["data"]["sms_code"],
        request_otp.json()["data"]["sms_insert"]["id"],
    )
    await state.update_data(phone_number=phone_number, sms_id=sms_id)
    await message.answer(lang["enter_your_otp_code"][current_locale] + str(otp_code))
    await state.set_state(Registration.otp)


@register_router.message(Registration.otp)
async def otp_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_locale = await locale(message, state)
    if not message.text.isdigit() and len(message.text) != 4:
        await message.answer(lang["invalid_otp_code"][current_locale])
        await state.set_state(Registration.otp)
        return
    response = requests.put(
        f"{settings.DOMAIN}/v1/confirmed_sms?id={data['sms_id']}&sms_code={int(message.text)}"
    )
    l.info(response.json())
    context = response.json()
    if context.get("data", None) is None:
        await message.answer(lang["incorrect_otp_code"][current_locale])
        await state.set_state(Registration.otp)
        return

    await message.answer(lang["enter_password"][current_locale])
    await state.set_state(Registration.password)


@register_router.message(Registration.password)
async def password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    current_locale = await locale(message, state)
    await silent_delete_message(message)
    data = await state.get_data()
    context = {
        "username": data["phone_number"],
        "password": data["password"],
        "id": data["sms_id"],
        "role": [settings.DEFAULT_ROLE_ID],
        "role_id": settings.DEFAULT_ROLE_ID,
    }
    l.info(context)
    response = requests.post(f"{settings.DOMAIN}/v1/register_user", json=context)
    await message.answer(
        lang["Registration_succeeded"][current_locale],
        reply_markup=get_user_menu("client"),
    )
    if response.status_code == 200:
        l.info(list(users_collection.find({})))
        l.info("User credentials are saved to daabase successfully...")
        l.info(response.json())
        users_collection.insert_one(
            get_context(
                message.from_user.id,
                response.json()["data"]["token"]["data"],
                data["phone_number"],
                data["password"],
                current_locale,
            )
        )
    else:
        await message.answer(lang["registration_failed"][current_locale])
    await state.clear()
