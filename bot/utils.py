from aiogram.exceptions import TelegramBadRequest
import requests
import logging
import re

from bot.nosql.config import users_collection
from bot.settings import settings


logger = logging.getLogger(__name__)


async def silent_delete_message(message):
    try:
        return await message.delete()
    except TelegramBadRequest:
        return


def get_user(user_id: int) -> dict:
    user = users_collection.find_one({"user_id": user_id})
    logger.info(user)
    if not user:
        logger.info("USER DOES NOT EXIST BROOOOOOOOOOOOOOOOOOOOOOO")
        return {"status": "NOT_REGISTERED"}

    credentials = user.get("credentials", {})
    token = credentials.get("token", {}).get("access_token")

    if not token:
        logger.info("THERE IS NO TOKEN +=====================================")
        credentials["status"] = "LOGGED_OUT"
        return credentials

    url = f"{settings.DOMAIN}/accounts/profile"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if (
        response.status_code == 200
        and response.json().get("data")
        and credentials["status"] != "LOGGED_OUT"
    ):
        credentials["status"] = "OK"
    else:
        credentials["status"] = "LOGGED_OUT"

    return credentials


def is_valid_phone_number(phone: str) -> bool:
    pattern = re.compile(r"^\+?\d{10,15}$")
    return pattern.match(phone) is not None


def get_phone_number(message):

    if message.content_type == "text":
        phone_number = message.text
    else:
        phone_number = message.contact.phone_number
    if not (
        phone_number.startswith("+998")
        and phone_number[1:].isdigit()
        and len(phone_number) in range(8, 15)
    ):
        return None
    return phone_number


async def locale(message, state=None):
    user = get_user(message.from_user.id)
    if user["status"] == "OK":
        return user["locale"]
    else:
        default = message.from_user.language_code
        data = await state.get_data()
        state_lang = data.get("locale", None)
        if state is None:
            return default
        if state_lang is None:
            return default
        return state_lang


def query_locale(message):
    user = get_user(message.chat.id)
    if user["status"] == "OK":
        return user["locale"]
    else:
        return message.from_user.language_code
