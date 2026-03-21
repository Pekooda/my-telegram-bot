import asyncio, os, logging, requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
bot = Bot(TOKEN)
dp = Dispatcher()
URL = "https://my-telegram-bot-on3x.onrender.com/"

@dp.message(Command("start"))
async def start(message: Message):
    logging.debug('T0')
    await message.answer("Carry on")

async def handle(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.debug("Webhook parse error:", e)
        return web.Response(text="Bad Request", status=400)

    return web.Response(text="OK", status=200)

async def alarms():
    await bot.send_message(PEKO_ID, "BOSTARTMESS")
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as resp:
                    logging.debug(f'ping NICE', resp.status)
        except Exception as e:
            logging.debug(f'ping reror: {e}')
        await asyncio.sleep(300)
async def bittest():
    while True:
        await bot.send_message(PEKO_ID, "SPAM")
        await asyncio.sleep(30)


async def main():
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="OK", status=200))
    app.router.add_post("/webhook", handle)
    logging.basicConfig(level=logging.DEBUG)
    asyncio.create_task(alarms())
    asyncio.create_task(bittest())
    await bot.set_webhook("https://my-telegram-bot-on3x.onrender.com/webhook")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())