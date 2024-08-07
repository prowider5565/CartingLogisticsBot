from fastapi import FastAPI, Request
from aiogram import types
from bot.config import dp, bot
from bot.settings import settings


app = FastAPI()

WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = f"{settings.HOST}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


@app.post(WEBHOOK_PATH)
async def bot_webhook_handler(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.WEB_HOST, port=settings.PORT)
