carting.uz-bot
├── bot
│   ├── db
│   ├── roles
│   │   ├── client
│   │   │   ├── generators
│   │   │   ├── handlers
│   │   │   │   ├── keyboards
│   │   │   │   │   ├── inline
│   │   │   │   │   └── reply
│   │   │   │   └── __init__.py
│   │   │   └── states
│   │   ├── company
│   │   │   ├── generators
│   │   │   ├── handlers
│   │   │   │   ├── keyboards
│   │   │   │   │   ├── inline
│   │   │   │   │   └── reply
│   │   │   │   └── __init__.py
│   │   │   └── states
│   │   ├── dispatcher
│   │   │   ├── generators
│   │   │   ├── handlers
│   │   │   │   ├── keyboards
│   │   │   │   │   ├── inline
│   │   │   │   │   └── reply
│   │   │   │   └── __init__.py
│   │   │   └── states
│   │   ├── general
│   │   │   ├── generators
│   │   │   ├── handlers
│   │   │   │   ├── keyboards
│   │   │   │   │   ├── inline
│   │   │   │   │   └── reply
│   │   │   │   └── __init__.py
│   │   │   └── states
│   │   ├── driver
│   │   │   ├── generators
│   │   │   ├── handlers
│   │   │   │   ├── keyboards
│   │   │   │   │   ├── inline
│   │   │   │   │   └── reply
│   │   │   │   └── __init__.py
│   │   │   └── states
│   ├── config.py
│   └── settings.py
├── .env
├── .gitignore
├── .gitlab-ci.yml
├── docker-compose.yml
├── Dockerfile
├── launcher.sh
├── main.py
├── README.md
└── requirements.txt











write a pagination based list of my loads here.










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











there should be message like this:






1. <first load name>
2. <second load name>
...

_________
under here there should be the indexes (1, 2) of the corresponding loads. then whenever I click on one of the inline buttons with indexes of the loads, it should show me the detail of the load. this is what I get from api:









{'error': None, 'message': None, 'timestamp': 1723787747727, 'status': 200, 'path': None, 'data': [{'id': '4c8e29df-8ffd-c91c-c228-89d078cb4207', 'created_at': None, 'created_by': 'c8df4de5-b49c-4a83-bd2f-2ad97413f4d9', 'updated_at': None, 'updated_by': None, 'state': 1, 'weight': 89, 'size': None, 'type': 'килограмм', 'name': 'New load', 'price': '44', 'phone_number': '+998945555555', 'pickup_latlong': '[20.659324,-11.406255]', 'delivery_latlong': '[20.659324,-11.406255]', 'send_region': 'Наманган', 'send_district': 'Янгикурган', 'receive_region': 'Ташкент', 'receive_district': 'Сергели', 'offer_id': None, 'client_phone': '+998945555555', 'client_fullname': '+998945555555', 'receiver_phone': '+998945555555', 'receiver_fullname': '+998945555555', 'load_status': 0, 'driver_id': None, 'client_id': None, 'dispatcher_id': None, 'organization_id': None, 'pickup_date': None, 'delivery_date': None, 'width': None, 'height': None, 'length': None, 'img_id': None, 'by_org': None}], 'response': None}








and also there should be next >> and << previous inline keyboards responsible for moving to the next and previous page. store the current page in query data like this callback_data=current_page + 1 for next button, - for previous button. then use it to  handle the next and previous buttons, inside the next and previous buttons, take that data from query and display the page from the list of personal loads you take from api.