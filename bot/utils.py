from aiogram.exceptions import TelegramBadRequest
import logging

from bot.nosql.config import users_collection


logger = logging.getLogger(__name__)


async def locale(state):
    data = await state.get_data()
    return data["lang"]


async def silent_delete_message(message):
    try:
        return await message.delete()
    except TelegramBadRequest:
        return


def get_user(user_id) -> dict:
    user = users_collection.find_one({"user_id": user_id})
    logger.info(list(users_collection.find({})))
    if user is None:
        return {}
    return user["credentials"]
