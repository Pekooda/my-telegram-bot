import asyncio, os, logging, requests, aiohttp, asyncpg
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
URL = "https://my-telegram-bot-on3x.onrender.com/webhook"
DATABASE_URL = os.getenv("DATABASE_URL")

@dp.message(Command("start"))
async def start(message: Message):
    logging.debug('T0')
    await message.answer("Carry on")

@dp.message(Command("count"))
async def count(message: Message):
    user_id = message.from_user.id
    await message.answer(f"Ща не ща ибо щаща")
    async with app["chest"].acquire() as conn:
        value = await conn.fetchval(
            """
            INSERT INTO counters (user_id, value)
            VALUES ($1, 1)
            ON CONFLICT (user_id)
            DO UPDATE SET value = counters.value + 1
            RETURNING value
            """,
            user_id,
        )
    await message.answer(f"Ща: {value}")


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

async def handle(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.debug("Webhook parse error:", e)
        return web.Response(text="Bad Request", status=400)
    return web.Response(text="OK", status=200)

async def on_startup(app):
    app["task1"] = asyncio.create_task(alarms())
    app["task2"] = asyncio.create_task(bittest())
    app["chest"] = await asyncpg.create_pool(dsn=DATABASE_URL)
    async with app["chest"].acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS counters (
                user_id BIGINT PRIMARY KEY,
                value BIGINT NOT NULL DEFAULT 0
            )
            """
        )
async def on_cleanup(app):
    await app["chest"].close()
    for name in ["task1", "task2"]:
        task = app.get(name)
        if task:
            task.cancel()
            try:
                await task
            except:
                pass


async def main():
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="OK", status=200))
    app.router.add_post("/webhook", handle)
    logging.basicConfig(level=logging.DEBUG)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    await bot.set_webhook(URL)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())