import asyncio, os, logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    logging.debug('T0')
    await message.answer("Carry")

async def handle(request):
    try:
        data = await request.json()
        await dp.feed_update(bot, data)
    except Exception as e:
        print("Webhook parse error:", e)
        return web.Response(text="Bad Request", status=400)

    return web.Response(text="OK", status=200)

#### БУДИЛЬНИКИ
async def alarms():
### Сообщение админу о включении
    await bot.send_message(PEKO_ID, "фыфыоброе утро!")


async def main():
    app = web.Application()
    app.router.add_post("/webhook", handle)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('T1')
    asyncio.create_task(alarms())
    logging.debug('T2')
    await bot.set_webhook("https://my-telegram-bot-on3x.onrender.com/webhook")
    logging.debug('T3')
    runner = web.AppRunner(app)
    logging.debug('T4')
    await runner.setup()
    logging.debug('T5')
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    logging.debug('T6')
    await site.start()
    logging.debug('T7')
    await asyncio.Event().wait()
    logging.debug('T8')

if __name__ == "__main__":
    asyncio.run(main())