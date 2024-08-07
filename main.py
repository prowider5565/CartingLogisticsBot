from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, types
from bot. import dp, bot

app = FastAPI()

WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = f"https://your-domain.com{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


@app.post(WEBHOOK_PATH)
async def process_webhook(request: Request):
    update = types.Update(**await request.json())
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    await dp.process_update(update)
    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
