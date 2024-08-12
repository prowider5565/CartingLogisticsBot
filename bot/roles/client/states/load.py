from aiogram.fsm.state import StatesGroup, State


# Define additional states for new fields
class LoadState(StatesGroup):
    name = State()
    weight = State()
    type = State()
    price = State()
    phone_number = State()
    pickup_latlong = State()
    delivery_latlong = State()
    send_region = State()
    send_district = State()
    receive_region = State()
    receive_district = State()
    client_phone = State()
    client_fullname = State()
    receiver_phone = State()
    receiver_fullname = State()
    width = State()
    length = State()
    height = State()
    pickup_date = State()
    delivery_date = State()
