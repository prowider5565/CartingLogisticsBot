from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from bot.roles.general.keyboards.reply.contact import share_contact_markup
from bot.roles.general.states.auth_state import Authentication
from bot.nosql.config import users_collection
from bot.utils import locale, logger as l
from bot.languages.general import lang
from bot.settings import settings

login_router = Router()


# @login_router.message()


