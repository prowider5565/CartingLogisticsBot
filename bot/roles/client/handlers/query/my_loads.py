from aiogram import Router, types
import requests

from bot.settings import settings
from bot.utils import get_user


loads_router = Router()


@loads_router.callback_query(lambda query: query.data == "my_loads")
async def my_loads_handler(query: types.CallbackQuery):
    url = f"{settings.DOMAIN}/my-loads"
    user = get_user(query.message.chat.id)
    token = user["token"]["access_token"]
    request = requests.get(url, headers={"Authorization": "Bearer {}".format(token)})
    await query.message.answer(str(request.json()))
