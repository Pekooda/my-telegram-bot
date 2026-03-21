import asyncio, os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Carry")

async def handle(request):
    data = await request.json()
    await dp.feed_update(bot, data)
    return web.Response()

async def main():
    app = web.Application()
    app.router.add_post("/webhook", handle)

    await bot.set_webhook("https://my-telegram-bot-on3x.onrender.com/webhook")

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())