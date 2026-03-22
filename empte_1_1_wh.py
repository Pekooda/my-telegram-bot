import asyncio, os, logging, requests, aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
bot = Bot(TOKEN)
dp = Dispatcher()
app = FastAPI()

@dp.message(Command("start"))
async def start(message: Message):
    logging.debug('T0')
    await message.answer("Carry on")

async def alarms():
    await bot.send_message(PEKO_ID, "BOSTARTMESS")
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=5) as resp:
                    logging.debug(f"ping NICE: {resp.status}")
        except Exception as e:
            logging.debug(f'ping RERORERO: {e}')
        await asyncio.sleep(300)
async def bittest():
    while True:
        await bot.send_message(PEKO_ID, "SPAM")
        await asyncio.sleep(30)

@app.post("/webhook")
async def handle(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.debug("Webhook parse error:", e)
        return {"ok": False}
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook("https://my-telegram-bot-pekooda6337-pamex4dh.leapcell.dev/webhook")
    app.state.tasks = [
        asyncio.create_task(alarms()),
        asyncio.create_task(bittest())
    ]

@app.on_event("shutdown")
async def on_cleanup():
    for task in app.state.tasks:
        task.cancel()
    for task in app.state.tasks:
        try:
            await task
        except asyncio.CancelledError:
            pass