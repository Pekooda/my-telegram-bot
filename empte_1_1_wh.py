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

app = FastAPI()

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
    await bot.set_webhook("https://my-telegram-bot-40.leapcell.dev/webhook")
    app["task1"] = asyncio.create_task(alarms())
    app["task2"] = asyncio.create_task(bittest())
@app.on_event("cleanup")
async def on_cleanup(app):
    for name in ["task1", "task2"]:
        task = app.get(name)
        if task:
            task.cancel()
            try:
                await task
            except:
                pass