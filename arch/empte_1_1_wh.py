import asyncio, os, logging, requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from typing import Union

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
bot = Bot(TOKEN)
dp = Dispatcher()
app = FastAPI()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Carry on")

#async def alarms():
#    await bot.send_message(PEKO_ID, "BOSTARTMESS")
#async def bittest():
#    while True:
#        await bot.send_message(PEKO_ID, "SPAM")
#        await asyncio.sleep(30)

async def alarms():
    await bot.send_message(PEKO_ID, "BOSTARTMESS")
async def bittest():
    while True:
        await bot.send_message(PEKO_ID, "SPAM")
        await asyncio.sleep(30)


@app.get("/kaithhealth")
@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def handle(request: Request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(f"Webhook error: {e}, data={data}")
    return {"ok": True}

URL = "https://my-telegram-bot-pekooda6337-pamex4dh.leapcell.dev/webhook"
@app.on_event("startup")
async def on_startup():
    try:
        info = await bot.get_webhook_info()
        if info.url != URL:
            await bot.set_webhook(URL)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
    if not hasattr(app.state, "tasks"):
        app.state.tasks = [
            asyncio.create_task(bittest())
        ]
        asyncio.create_task(alarms())

@app.on_event("shutdown")
async def on_shutdown():
    for task in getattr(app.state, "tasks", []):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass