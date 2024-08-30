from aiogram import Router, types
import requests

from bot.utils import logger as l, get_user
from bot.settings import settings


init_router = Router()


def get_offer_id(response, load_id):
    l.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    l.info(response)
    l.info(load_id)
    l.info("LOAD ID ABOVE")
    # Check if 'data' exists in the response
    if "data" in response.keys():
        l.info("DATA KEY IS IN THE RESOPNSE <===============>")
        # Iterate through each offer in the data list
        for offer in response["data"]:
            l.info("ITERATING THROUGH DATA <===============>")
            # If the load_id matches, return the corresponding id
            if offer.get("load_id") == load_id:
                l.info(
                    f"GETTING OFFER ID AND USER ID <===============>, {offer.get('id')} {offer.get('created_by')}"
                )
                return offer.get("id"), offer.get("created_by")

    # Return None if no match is found
    return None, None


@init_router.callback_query(lambda query: query.data.startswith("lico"))
async def confirm_load_delivery_handler(query: types.CallbackQuery):
    user = get_user(query.message.chat.id)
    l.info("IN CORRECT PLACE")
    l.info(query.data)
    load_id, balance = query.data.split(":")[1:]
    offer_fetch_url = f"{settings.DOMAIN}/get/offer/for/client?offer_status=active"
    headers = {"Authorization": f"Bearer {user['token']['access_token']}"}
    fetch_offer_request = requests.get(url=offer_fetch_url, headers=headers)
    offer_id, user_id = get_offer_id(fetch_offer_request.json(), load_id)
    if offer_id is not None and user_id is not None:
        status_url = f"{settings.DOMAIN}/offers/update-status"
        offer_url = f"{settings.DOMAIN}/update/all/offer/"
        data = {
            "id": offer_id,
            "offer_status": "active",
            "load_status": 0,
            "balance": balance,
        }
        offer_data = {"user_id": user_id, "load_id": load_id}
        request = requests.patch(status_url, json=data, headers=headers)
        l.info(request.status_code)
        l.info(request.json())
        offer_request = requests.put(offer_url, json=offer_data, headers=headers)
        l.info(offer_request.status_code)
        l.info(offer_request.json())
        await query.message.answer(
            f"status: {request.status_code} {offer_request.status_code}"
        )
    else:
        await query.message.answer("Offer not found or already accepted.")
