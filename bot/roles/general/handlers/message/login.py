from aiogram.fsm.context import FSMContext
from aiogram import Router, types
import requests

from bot.utils import get_user, silent_delete_message, logger as l, locale
from bot.roles.general.generators.get_scheme import get_context
from bot.roles.general.states.login_state import LoginState
from bot.nosql.config import users_collection
from bot.languages.general import lang
from bot.settings import settings


login_router = Router()


# @login_router.message(LoginState.phone_number)
# async def phone_number_handler(message: types.Message, state: FSMContext):
#     user = get_user(message.from_user.id)
#     phone_number = get_phone_number(message)
#     if phone_number is None:
#         # await message.answer(lang["invalid_phone_number"][user["locale"]])
#         await message.answer("Invalid phone number")
#         await state.set_state(LoginState.phone_number)
#         return
#     phone_number = phone_number[1:]
#     await state.update_data(phone_number=phone_number)
#     # await message.answer(lang["enter_password"][user["locale"]])
#     await message.answer("Enter password")
#     await state.set_state(LoginState.password)


@login_router.message(LoginState.password)
async def password_handler(message: types.Message, state: FSMContext):
    password = message.text
    user = get_user(message.from_user.id)
    if user["status"] != "NOT_REGISTERED":
        phone_number = user["phone_number"]
    else:
        data = await state.get_data()
        phone_number = data["phone_number"]
    await silent_delete_message(message)
    url = f"{settings.DOMAIN}/login/user"
    response = requests.post(url, data={"username": phone_number, "password": password})
    if response.status_code == 200:
        if user.get("credentials", None) is not None:
            users_collection.update_one(
                {"user_id": message.from_user.id},
                {
                    "$set": {
                        "credentials.status": "OK",
                        "credentials.token": response.json()["data"]["data"],
                    }
                },
            )
            l.info("THE UPDATED USER &&&&&&&&&&&&&&&&&&&")
            l.info(users_collection.find_one({"user_id": message.from_user.id}))
        else:
            l.info("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
            l.info(response.json())
            users_collection.insert_one(
                get_context(
                    message.from_user.id,
                    response.json()["data"]["data"],
                    phone_number,
                    password,
                    await locale(state),
                )
            )
        await message.answer(str(response.json()))
    else:
        await message.answer(lang["wrong_password"][await locale(state)])
        await state.set_state(LoginState.password)


{
    "error": None,
    "message": None,
    "timestamp": 1723275662604,
    "status": 200,
    "path": None,
    "data": {
        "status": "OK",
        "timestamp": 1723275662602,
        "data": {
            "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJ1cGRhdGVfaWQiOjEwNDkyMiwic3ViIjoiNGM4YTEyZGUtY2E1NS00ZmJjLTkwMzAtMzQzYjViZjc0YzdiIiwicm9sZXMiOiJDbGllbnQiLCJpc3MiOiIiLCJ0eXBlIjoiQmVhcmVyIiwibG9jYWxlIjoidXoiLCJzaWQiOiI0YWU3OGRkNS00YjA3LTQ0MTQtYThiMC1lNzVmMzhmZjkzYjQiLCJhdWQiOiJhY2NvdW50IiwiZnVsbF9uYW1lIjoiTkVXIFVTRVIiLCJleHAiOjE3MjMyOTM2NjIsInNlc3Npb25fc3RhdGUiOiJTVEFURUxFU1MiLCJpYXQiOjE3MjMyNzU2NjIsImp0aSI6IjExZWEyNmQwLTkzNWItNGFlNC1iOGQwLWU5MDA0Zjg4ODcyZCIsInVzZXJuYW1lIjoiOTk4MTUxOTU4ODcifQ.FBqajQWvKt8swcmQJnd9raIZ1r8p4KmUQC9IUoAa-xd8c5KXljmlYsP--9LRYlbo0PA4aKZanp4lnGygyWGLfGPqR0KaeE-_p3wJtaTKmlfn_KIttIdMW7kjCT9aVn5goYrITKP9Cfa7ABDsXHhSaemuT_RjNZCb1R9A5ziypmDFeYQZgSvsl8obo3_K__iPSw28U1KvOYEhVhvRmA5uizUeYL3DQIKGhuc75GLSeZnz-7_irWAZb4PvZ7P_bRhvxaOMOs1npj01KNcfmxHN36G2PDg4H7RyiLMyJ8yySSna4m2ZaEK66wg6l5qV1UwaKx9I5R0oJOKi62DrgYMIXw",
            "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0YzhhMTJkZS1jYTU1LTRmYmMtOTAzMC0zNDNiNWJmNzRjN2IiLCJhdWQiOiJhY2NvdW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL2dhdGV3YXkvcGxhdG9uLWF1dGgvcmVhbG1zL2RldiIsImV4cCI6MTcyMzI5MzY2Miwic2Vzc2lvbl9zdGF0ZSI6IlNUQVRFTEVTUyIsImlhdCI6MTcyMzI3NTY2MiwianRpIjoiMTFlYTI2ZDAtOTM1Yi00YWU0LWI4ZDAtZTkwMDRmODg4NzJkIiwic2lkIjoiNGFlNzhkZDUtNGIwNy00NDE0LWE4YjAtZTc1ZjM4ZmY5M2I0IiwidXNlcm5hbWUiOiI5OTgxNTE5NTg4NyJ9.TA2hGiPU3trkBR8b7G6evz9ldzjeIhCCzhPhmAAAvcQ1FMrdaf-RF9kgq0r-ibqX8KuYmy6Rcs5PtRASmhxslIgSnwWC0v5Hy5yAC484QCrp7zbG4znG4Tu3OTdyJDh0_oaN-wf8ILwzB-oFKfUM69yy-37RE1zV4JKRQfgSaWGdQHSnbR-l3-woDNx2K3vOWLrFehDnJBwLey17oMdGK_sVbMLCxmacXcakKVUfVdJPXIe1LYaAbt4GTM8V0mGk8__713fqrBTb6MTZo4E1ZufDTT7Upnz_zPXsQwTFf3XnfkRCeKbEFj_iPyFPQHTH1mMDJ7gdcxfLwJ89Vjassw",
            "token_type": "Bearer",
            "expires_in": 18000000,
            "refresh_expires_in": 18000000,
        },
    },
    "response": None,
}
