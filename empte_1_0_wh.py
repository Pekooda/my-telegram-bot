#### ВЕРСИИ:
# 1.0.wh - тест вебхука

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, os, requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web
from dotenv import load_dotenv


### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
bot = Bot(TOKEN_KEY)
dp = Dispatcher()
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
URL = "https://my-telegram-bot-on3x.onrender.com/"


#### КОМАНДЫ БОТА
### Начало жизни
async def start(message: types.Message, args: str):
    await message.answer(f"Я работаю. НЕТ")

@dp.message()
async def vse(message: Message):
    if message.text and message.text.startswith("/"):
        parts = message.text.split(maxsplit=1)
        cmd_with_slash = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cmd = cmd_with_slash.lstrip("/").split("@", 1)[0].lower()
        commanda = globals().get(cmd)
        if commanda:
            await commanda(message, args)

#### БУДИЛЬНИКИ
async def alarms():
### Сообщение админу о включении
    await bot.send_message(PEKO_ID, "доброе утро! НЕТ")
    while True:
        try:
            requests.get(URL, timeout=5)
        except:
            time.sleep(600)


async def handle(request):
    data = await request.json()
    await dp.feed_update(bot, data)
    return web.Response()

####запись и запуск бота
async def main():
    app = web.Application()
    app.router.add_post("/webhook", handle)
    asyncio.create_task(alarms())
    await bot.set_webhook("https://my-telegram-bot-on3x.onrender.com/webhook")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await asyncio.Event().wait()




if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"я спать пошла, спокойной ночи\n")