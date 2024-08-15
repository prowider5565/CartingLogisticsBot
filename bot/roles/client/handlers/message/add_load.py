from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import Message
import requests

from bot.roles.client.keyboards.reply.location import get_share_location_markup
from bot.roles.client.keyboards.reply.load_type import get_type_markup
from bot.roles.general.keyboards.inline.user_menu import get_user_menu
from bot.utils import is_valid_phone_number, get_user, isfloat
from bot.roles.client.states.load import LoadState
from bot.languages.client import lang
from bot.settings import settings
from bot.roles.client.generators.regions import (
    get_districts_keyboard,
    get_regions_keyboard,
)

load_router = Router()


def translate(key, user_id):
    user = get_user(user_id)
    language = user["locale"]
    return lang.get(key, {}).get(language, "en")


@load_router.message(LoadState.name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        translate("enter_weight", message.from_user.id),
        reply_markup=get_regions_keyboard(message.from_user.id),
    )
    await state.set_state(LoadState.weight)


@load_router.message(LoadState.weight)
async def weight_handler(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    if not isfloat(message.text):
        await message.answer(translate("invalid_weight", message.from_user.id))
        await state.set_state(LoadState.weight)
        return
    await message.answer(translate("enter_width", message.from_user.id))
    await state.set_state(LoadState.width)


@load_router.message(LoadState.width)
async def width_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(translate("invalid_width", message.from_user.id))
        await state.set_state(LoadState.width)
        return
    await state.update_data(width=message.text)
    await message.answer(translate("enter_length", message.from_user.id))
    await state.set_state(LoadState.length)


@load_router.message(LoadState.length)
async def length_handler(message: Message, state: FSMContext):
    await state.update_data(length=message.text)
    await message.answer(translate("enter_height", message.from_user.id))
    await state.set_state(LoadState.height)


@load_router.message(LoadState.height)
async def height_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(translate("invalid_height", message.from_user.id))
        await state.set_state(LoadState.height)
        return
    await state.update_data(height=message.text)
    await message.answer(
        translate("select_load_type", message.from_user.id),
        reply_markup=get_type_markup(message.from_user.id),
    )
    await state.set_state(LoadState.type)


@load_router.message(LoadState.type)
async def type_handler(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer(translate("enter_price", message.from_user.id))
    await state.set_state(LoadState.price)


@load_router.message(LoadState.price)
async def price_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(translate("invalid_price", message.from_user.id))
        await state.set_state(LoadState.price)
        return
    await state.update_data(price=message.text)
    await message.answer(translate("enter_phone_number", message.from_user.id))
    await state.set_state(LoadState.phone_number)


@load_router.message(LoadState.phone_number)
async def phone_number_handler(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not is_valid_phone_number(message.text):
        await message.answer(translate("invalid_phone_number", message.from_user.id))
        return
    await state.update_data(phone_number=message.text)
    await message.answer(
        translate("share_pickup_location", message.from_user.id),
        reply_markup=get_share_location_markup(user["locale"]),
    )
    await state.set_state(LoadState.pickup_latlong)


@load_router.message(LoadState.pickup_latlong, F.location)
async def pickup_latlong_handler(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await state.update_data(
        pickup_latlong=(message.location.latitude, message.location.longitude)
    )
    await message.answer(
        translate("share_delivery_location", message.from_user.id),
        reply_markup=get_share_location_markup(user["locale"]),
    )
    await state.set_state(LoadState.delivery_latlong)


@load_router.message(LoadState.delivery_latlong, F.location)
async def delivery_latlong_handler(message: types.Message, state: FSMContext):
    await state.update_data(
        delivery_latlong=(message.location.latitude, message.location.longitude)
    )
    await message.answer(translate("enter_pickup_date", message.from_user.id))
    await state.set_state(LoadState.pickup_date)


@load_router.message(LoadState.pickup_date)
async def pickup_date_handler(message: Message, state: FSMContext):
    await state.update_data(pickup_date=message.text)
    await message.answer(translate("enter_delivery_date", message.from_user.id))
    await state.set_state(LoadState.delivery_date)


@load_router.message(LoadState.delivery_date)
async def delivery_date_handler(message: Message, state: FSMContext):
    await state.update_data(delivery_date=message.text)
    await message.answer(
        translate("select_send_region", message.from_user.id),
        reply_markup=get_regions_keyboard(message.from_user.id),
    )
    await state.set_state(LoadState.send_region)


@load_router.message(LoadState.send_region)
async def send_region_handler(message: Message, state: FSMContext):
    await state.update_data(send_region=message.text)
    await message.answer(
        translate("enter_send_district", message.from_user.id),
        reply_markup=get_districts_keyboard(message.from_user.id, message.text),
    )
    await state.set_state(LoadState.send_district)


@load_router.message(LoadState.send_district)
async def send_district_handler(message: Message, state: FSMContext):
    await state.update_data(send_district=message.text)
    await message.answer(
        translate("select_receive_region", message.from_user.id),
        reply_markup=get_regions_keyboard(message.from_user.id),
    )
    await state.set_state(LoadState.receive_region)


@load_router.message(LoadState.receive_region)
async def receive_region_handler(message: Message, state: FSMContext):
    await state.update_data(receive_region=message.text)
    await message.answer(
        translate("enter_receive_district", message.from_user.id),
        reply_markup=get_districts_keyboard(message.from_user.id, message.text),
    )
    await state.set_state(LoadState.receive_district)


@load_router.message(LoadState.receive_district)
async def receive_district_handler(message: Message, state: FSMContext):
    await state.update_data(receive_district=message.text)
    await message.answer(translate("enter_client_phone", message.from_user.id))
    await state.set_state(LoadState.client_phone)


@load_router.message(LoadState.client_phone)
async def client_phone_handler(message: Message, state: FSMContext):
    if not is_valid_phone_number(message.text):
        await message.answer(translate("invalid_phone_number", message.from_user.id))
        return
    await state.update_data(client_phone=message.text)
    await message.answer(translate("enter_client_fullname", message.from_user.id))
    await state.set_state(LoadState.client_fullname)


@load_router.message(LoadState.client_fullname)
async def client_fullname_handler(message: Message, state: FSMContext):
    await state.update_data(client_fullname=message.text)
    await message.answer(translate("enter_receiver_phone", message.from_user.id))
    await state.set_state(LoadState.receiver_phone)


@load_router.message(LoadState.receiver_phone)
async def receiver_phone_handler(message: Message, state: FSMContext):
    if not is_valid_phone_number(message.text):
        await message.answer(translate("invalid_phone_number", message.from_user.id))
        return
    await state.update_data(receiver_phone=message.text)
    await message.answer(translate("enter_receiver_fullname", message.from_user.id))
    await state.set_state(LoadState.receiver_fullname)


@load_router.message(LoadState.receiver_fullname)
async def receiver_fullname_handler(message: Message, state: FSMContext):
    await state.update_data(receiver_fullname=message.text)
    user_data = await state.get_data()
    url = f"{settings.DOMAIN}/loads/create"
    user = get_user(message.from_user.id)
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    request = requests.post(url, json=user_data, headers=headers)
    if request.status_code == 200:
        await message.answer(
            lang["load_successfully_created"](user_data)[user["locale"]],
            reply_markup=get_user_menu(user["role"]["label"], user["locale"]),
        )
    else:
        await message.answer(
            lang["error_in_creating_load"](request.json()["message"])[user["locale"]]
        )
    await state.clear()
