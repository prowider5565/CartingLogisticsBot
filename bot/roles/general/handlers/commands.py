from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router

from bot.roles.general.keyboards.inline.user_menu import user_menu_markup
from bot.roles.general.keyboards.reply.lang import language_keyboards
from bot.roles.general.states.login_state import LoginState
from bot.middleware.auth import AuthenticationMiddleware
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.utils import get_user, logger as l


command_router = Router()
command_router.message.middleware(AuthenticationMiddleware())


@command_router.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    greeting = lang["warm_greeting"](message.from_user.full_name)[user["locale"]]
    l.info(list(users_collection.find({"user_id": message.from_user.id})))
    l.info("USER:            " + str(user))
    await message.answer(greeting, reply_markup=user_menu_markup(user["locale"]))


@command_router.message(Command("/flushall"))
async def flush_all(message: types.Message, state: FSMContext):
    users_collection.delete_many({})
    await message.answer("All data has been deleted successfully!")


@command_router.message(Command("manual_login"))
async def manual_login_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter phone number")
    await state.set_state(LoginState.phone_number)


# [
#     {
#         "_id": ObjectId("66b68de48b7f7620b50e13e9"),
#         "user_id": 2003049919,
#         "credentials": {
#             "token": {
#                 "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJ1cGRhdGVfaWQiOjcyNiwic3ViIjoiNjZmZTI5OTItMWE4My00ZjM2LTk4NjYtNWMyM2VjMjZhZDRhIiwicm9sZXMiOiJQbGF0b24gQWRtaW5zLCBEcml2ZXIsIENsaWVudCIsImlzcyI6IiIsInR5cGUiOiJCZWFyZXIiLCJsb2NhbGUiOiJ1eiIsInNpZCI6ImE0MTFkNDE3LTljYjUtNDdhNC1hZjY3LThiODAyZjFiOGFhNCIsImF1ZCI6ImFjY291bnQiLCJmdWxsX25hbWUiOiJCZWd6b2QiLCJleHAiOjE3MjMyNTc5MDgsInNlc3Npb25fc3RhdGUiOiJTVEFURUxFU1MiLCJpYXQiOjE3MjMyMzk5MDgsImp0aSI6IjliZDMzZTJiLTFjNDMtNDU4Yy04Njc1LTdkMWVkZjNhMWIwMyIsInVzZXJuYW1lIjoiYmVrem9kIn0.flVFqyMplCcIKFqXaIwpHSbi2y3T013AY1OF16XHU5iwZmio28z0BfmoQ7HG9k2hXmSb7_Jabhxh8vRAoryYdn-I7546p-oTHhE1e79PE6cjGS-bL10PPULy7A1RQC85JkcqyuOSUIYFgMoemmTOru2LKwVy64ZwQc1tP-H49_LOLFcYDTnugwxPOydI4lFM6aAXY3yzXVGzTn6hzsCszJ4YQaqBTVIc0GWfXehAS0AWUjviRowmO-yrzedCeBCCKN4FzjHSIO3F7wWI08x_04ncd0R_YUXOfaLcDkBb2jzkiBVOxLxWB2Xzs_5RFD8gFnzdlL9Ay_fAAc09MLBlqA",
#                 "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2NmZlMjk5Mi0xYTgzLTRmMzYtOTg2Ni01YzIzZWMyNmFkNGEiLCJhdWQiOiJhY2NvdW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL2dhdGV3YXkvcGxhdG9uLWF1dGgvcmVhbG1zL2RldiIsImV4cCI6MTcyMzI1NzkwOCwic2Vzc2lvbl9zdGF0ZSI6IlNUQVRFTEVTUyIsImlhdCI6MTcyMzIzOTkwOCwianRpIjoiOWJkMzNlMmItMWM0My00NThjLTg2NzUtN2QxZWRmM2ExYjAzIiwic2lkIjoiYTQxMWQ0MTctOWNiNS00N2E0LWFmNjctOGI4MDJmMWI4YWE0IiwidXNlcm5hbWUiOiJiZWt6b2QifQ.2QvTN7OYPMltmBS8K7QMP-YTFqkq0gHWkdyLUqQhIJspwexBMmmT0RVCDUDK6OmJKJ3dMNPaH_DE_-wgezjTsLJWtB845xstnMh0EdxFgV2A2WuZrYrRZD5TOCb1tzYHx9EBOFlonl5nFRCa7CnD4R2TnQN12KiMLrOplIaQ3BgYNnbBrIY8QxlyIMAgosvQCa5xXvwtsKlb2jsJyBlKxsivGO3koJN2helqU8ghfJPP6PStivYr1eMF60OCdHKBYeVArlcaaNF0eIPRaABig8f48sZA-H2Y-2U6Cq_NcUMpXMRa0kMih8dWO076oaJmYiBXZx4K5p6jmoqYC1oSAw",
#                 "token_type": "Bearer",
#                 "expires_in": 18000000,
#                 "refresh_expires_in": 18000000,
#             },
#             "phone_number": "99896669774",
#             "password": "123456789",
#             "locale": "uz",
#             "status": "LOGGED_OUT",
#         },
#     }
# ]

# {
#     "token": {
#         "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJ1cGRhdGVfaWQiOjcyNiwic3ViIjoiNjZmZTI5OTItMWE4My00ZjM2LTk4NjYtNWMyM2VjMjZhZDRhIiwicm9sZXMiOiJQbGF0b24gQWRtaW5zLCBEcml2ZXIsIENsaWVudCIsImlzcyI6IiIsInR5cGUiOiJCZWFyZXIiLCJsb2NhbGUiOiJ1eiIsInNpZCI6ImE0MTFkNDE3LTljYjUtNDdhNC1hZjY3LThiODAyZjFiOGFhNCIsImF1ZCI6ImFjY291bnQiLCJmdWxsX25hbWUiOiJCZWd6b2QiLCJleHAiOjE3MjMyNTc5MDgsInNlc3Npb25fc3RhdGUiOiJTVEFURUxFU1MiLCJpYXQiOjE3MjMyMzk5MDgsImp0aSI6IjliZDMzZTJiLTFjNDMtNDU4Yy04Njc1LTdkMWVkZjNhMWIwMyIsInVzZXJuYW1lIjoiYmVrem9kIn0.flVFqyMplCcIKFqXaIwpHSbi2y3T013AY1OF16XHU5iwZmio28z0BfmoQ7HG9k2hXmSb7_Jabhxh8vRAoryYdn-I7546p-oTHhE1e79PE6cjGS-bL10PPULy7A1RQC85JkcqyuOSUIYFgMoemmTOru2LKwVy64ZwQc1tP-H49_LOLFcYDTnugwxPOydI4lFM6aAXY3yzXVGzTn6hzsCszJ4YQaqBTVIc0GWfXehAS0AWUjviRowmO-yrzedCeBCCKN4FzjHSIO3F7wWI08x_04ncd0R_YUXOfaLcDkBb2jzkiBVOxLxWB2Xzs_5RFD8gFnzdlL9Ay_fAAc09MLBlqA",
#         "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2NmZlMjk5Mi0xYTgzLTRmMzYtOTg2Ni01YzIzZWMyNmFkNGEiLCJhdWQiOiJhY2NvdW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL2dhdGV3YXkvcGxhdG9uLWF1dGgvcmVhbG1zL2RldiIsImV4cCI6MTcyMzI1NzkwOCwic2Vzc2lvbl9zdGF0ZSI6IlNUQVRFTEVTUyIsImlhdCI6MTcyMzIzOTkwOCwianRpIjoiOWJkMzNlMmItMWM0My00NThjLTg2NzUtN2QxZWRmM2ExYjAzIiwic2lkIjoiYTQxMWQ0MTctOWNiNS00N2E0LWFmNjctOGI4MDJmMWI4YWE0IiwidXNlcm5hbWUiOiJiZWt6b2QifQ.2QvTN7OYPMltmBS8K7QMP-YTFqkq0gHWkdyLUqQhIJspwexBMmmT0RVCDUDK6OmJKJ3dMNPaH_DE_-wgezjTsLJWtB845xstnMh0EdxFgV2A2WuZrYrRZD5TOCb1tzYHx9EBOFlonl5nFRCa7CnD4R2TnQN12KiMLrOplIaQ3BgYNnbBrIY8QxlyIMAgosvQCa5xXvwtsKlb2jsJyBlKxsivGO3koJN2helqU8ghfJPP6PStivYr1eMF60OCdHKBYeVArlcaaNF0eIPRaABig8f48sZA-H2Y-2U6Cq_NcUMpXMRa0kMih8dWO076oaJmYiBXZx4K5p6jmoqYC1oSAw",
#         "token_type": "Bearer",
#         "expires_in": 18000000,
#         "refresh_expires_in": 18000000,
#     },
#     "phone_number": "99896669774",
#     "password": "123456789",
#     "locale": "uz",
#     "status": "OK",
# }
