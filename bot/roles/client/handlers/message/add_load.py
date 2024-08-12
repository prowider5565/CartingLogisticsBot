from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import Message
import requests

from bot.roles.client.keyboards.reply.location import share_location_markup
from bot.roles.client.generators.regions import get_regions_keyboard
from bot.utils import is_valid_phone_number, get_user
from bot.roles.client.states.load import LoadState
from bot.settings import settings


load_router = Router()


@load_router.message(LoadState.name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Please enter the weight:")
    await state.set_state(LoadState.weight)


@load_router.message(LoadState.weight)
async def weight_handler(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    if not message.text.isdigit():
        await message.answer("Invalid weight. Please enter a number.")
        await state.set_state(LoadState.weight)
        return
    await message.answer("Please enter the width:")
    await state.set_state(LoadState.width)


@load_router.message(LoadState.width)
async def width_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Invalid width. Please enter a number.")
        await state.set_state(LoadState.width)
        return
    await state.update_data(width=message.text)
    await message.answer("Please enter the length:")
    await state.set_state(LoadState.length)


@load_router.message(LoadState.length)
async def length_handler(message: Message, state: FSMContext):
    await state.update_data(length=message.text)
    await message.answer("Please enter the height:")
    await state.set_state(LoadState.height)


@load_router.message(LoadState.height)
async def height_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Invalid height. Please enter a number.")
        await state.set_state(LoadState.height)
        return
    await state.update_data(height=message.text)
    await message.answer("Please enter the type:")
    await state.set_state(LoadState.type)


@load_router.message(LoadState.type)
async def type_handler(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Please enter the price:")
    await state.set_state(LoadState.price)


@load_router.message(LoadState.price)
async def price_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Invalid price. Please enter a number.")
        await state.set_state(LoadState.price)
        return
    await state.update_data(price=message.text)
    await message.answer("Please enter the phone number:")
    await state.set_state(LoadState.phone_number)


@load_router.message(LoadState.phone_number)
async def phone_number_handler(message: Message, state: FSMContext):
    if not is_valid_phone_number(message.text):
        await message.answer(
            "Invalid phone number. Please enter a valid phone number with the country code:"
        )
        return
    await state.update_data(phone_number=message.text)
    await message.answer(
        "Please share your location for pickup latitude and longitude:",
        reply_markup=share_location_markup,
    )
    await state.set_state(LoadState.pickup_latlong)


@load_router.message(LoadState.pickup_latlong, F.location)
async def pickup_latlong_handler(message: types.Message, state: FSMContext):
    await state.update_data(
        pickup_latlong=(message.location.latitude, message.location.longitude)
    )
    await message.answer(
        "Please share your location for delivery latitude and longitude:",
        reply_markup=share_location_markup,
    )
    await state.set_state(LoadState.delivery_latlong)


@load_router.message(LoadState.delivery_latlong, F.location)
async def delivery_latlong_handler(message: types.Message, state: FSMContext):
    await state.update_data(
        delivery_latlong=(message.location.latitude, message.location.longitude)
    )
    await message.answer("Please enter the pickup date (YYYY-MM-DD):")
    await state.set_state(LoadState.pickup_date)


@load_router.message(LoadState.pickup_date)
async def pickup_date_handler(message: Message, state: FSMContext):
    await state.update_data(pickup_date=message.text)
    await message.answer("Please enter the delivery date (YYYY-MM-DD):")
    await state.set_state(LoadState.delivery_date)


@load_router.message(LoadState.delivery_date)
async def delivery_date_handler(message: Message, state: FSMContext):
    await state.update_data(delivery_date=message.text)
    await message.answer(
        "Please select the sending region:", reply_markup=get_regions_keyboard()
    )
    await state.set_state(LoadState.send_region)


@load_router.message(LoadState.send_region)
async def send_region_handler(message: Message, state: FSMContext):
    await state.update_data(send_region=message.text)
    await message.answer("Please enter the sending district:")
    await state.set_state(LoadState.send_district)


@load_router.message(LoadState.send_district)
async def send_district_handler(message: Message, state: FSMContext):
    await state.update_data(send_district=message.text)
    await message.answer(
        "Please select the receiving region:", reply_markup=get_regions_keyboard()
    )
    await state.set_state(LoadState.receive_region)


@load_router.message(LoadState.receive_region)
async def receive_region_handler(message: Message, state: FSMContext):
    await state.update_data(receive_region=message.text)
    await message.answer("Please enter the receiving district:")
    await state.set_state(LoadState.receive_district)


@load_router.message(LoadState.receive_district)
async def receive_district_handler(message: Message, state: FSMContext):
    await state.update_data(receive_district=message.text)
    await message.answer("Please enter the client's phone number:")
    await state.set_state(LoadState.client_phone)


@load_router.message(LoadState.client_phone)
async def client_phone_handler(message: Message, state: FSMContext):
    if not is_valid_phone_number(message.text):
        await message.answer(
            "Invalid phone number. Please enter a valid phone number with the country code:"
        )
        return
    await state.update_data(client_phone=message.text)
    await message.answer("Please enter the client's full name:")
    await state.set_state(LoadState.client_fullname)


@load_router.message(LoadState.client_fullname)
async def client_fullname_handler(message: Message, state: FSMContext):
    await state.update_data(client_fullname=message.text)
    await message.answer("Please enter the receiver's phone number:")
    await state.set_state(LoadState.receiver_phone)


@load_router.message(LoadState.receiver_phone)
async def receiver_phone_handler(message: Message, state: FSMContext):
    if not is_valid_phone_number(message.text):
        await message.answer(
            "Invalid phone number. Please enter a valid phone number with the country code:"
        )
        return
    await state.update_data(receiver_phone=message.text)
    await message.answer("Please enter the receiver's full name:")
    await state.set_state(LoadState.receiver_fullname)


@load_router.message(LoadState.receiver_fullname)
async def receiver_fullname_handler(message: Message, state: FSMContext):
    await state.update_data(receiver_fullname=message.text)
    # At this point, all data is collected
    user_data = await state.get_data()
    user = get_user(message.from_user.id)
    url = f"{settings.DOMAIN}/loads/create"
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    request = requests.post(url, json=user_data, headers=headers)
    await message.answer(str(request.json()) + str(request.status_code))
    await message.answer(str(user_data))
    # Finish the state
    await state.clear()
