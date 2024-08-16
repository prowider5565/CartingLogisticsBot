from aiogram import Router, types
import requests

from bot.roles.general.keyboards.reply.back_button import get_inline_back
from bot.roles.client.generators.pagination import get_loads_markup
from bot.middleware.auth import AuthenticationMiddleware
from bot.utils import get_user, logger as l
from bot.constants import ITEMS_PER_PAGE
from bot.settings import settings


loads_router = Router()
loads_router.message.middleware.register(AuthenticationMiddleware())


@loads_router.callback_query(lambda query: query.data.startswith("my_loads"))
async def my_loads_handler(query: types.CallbackQuery):
    # Handle case where the callback data is "my_loads" without a page number
    data_parts = query.data.split("_")

    if len(data_parts) == 2 and data_parts[1] == "loads":
        current_page = 1  # Default to page 1 if no page number is provided
    else:
        current_page = int(data_parts[-1])

    user = get_user(query.message.chat.id)
    token = user["token"]["access_token"]
    url = f"{settings.DOMAIN}/my-loads"
    request = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    loads = request.json().get("data", [])

    # Paginate loads
    start_index = (current_page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    paginated_loads = loads[start_index:end_index]

    # Create message
    message_text = "\n".join(
        [f"{i + 1}. {load['name']}" for i, load in enumerate(paginated_loads)]
    )

    # Update message with loads and navigation buttons
    await query.message.edit_text(
        message_text, reply_markup=get_loads_markup(paginated_loads, current_page)
    )


@loads_router.callback_query(lambda query: query.data.startswith("load_detail_"))
async def load_detail_handler(query: types.CallbackQuery):
    data_parts = query.data.split("_")
    l.info(data_parts)

    # Ensure there are exactly 3 parts: 'load_detail', current_page, and index
    if len(data_parts) != 4:
        await query.message.answer("Invalid load detail callback data.")
        return

    current_page, index = data_parts[2:]
    current_page = int(current_page)
    index = int(index)

    user = get_user(query.message.chat.id)
    token = user["token"]["access_token"]
    url = f"{settings.DOMAIN}/my-loads"
    request = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    loads = request.json().get("data", [])

    # Calculate the actual index of the load in the full list
    load_index = (current_page - 1) * ITEMS_PER_PAGE + index
    if load_index >= len(loads):
        await query.message.answer("The load index is out of range.")
        return

    load = loads[load_index]

    # Create load detail message
    load_detail = (
        f"Name: {load['name']}\n"
        f"Price: {load['price']}\n"
        f"Phone: {load['phone_number']}\n"
        f"Send Region: {load['send_region']}, {load['send_district']}\n"
        f"Receive Region: {load['receive_region']}, {load['receive_district']}"
    )

    await query.message.answer(
        load_detail, reply_markup=get_inline_back(user["locale"])
    )
