#### ВЕРСИИ:
# 1.0.wh - тест вебхука

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, os, requests, time
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web
from dotenv import load_dotenv


### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
bot = Bot("TOKEN_KEY")
dp = Dispatcher()
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
URL = "https://my-telegram-bot-on3x.onrender.com/"


#### КОМАНДЫ БОТА
### Начало жизни
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Я работаю.")


#### БУДИЛЬНИКИ
async def alarms():
### Сообщение админу о включении
    await bot.send_message(PEKO_ID, "доброе утро!")
    while True:
        try:
            requests.get(URL, timeout=5)
            print("ping ok")
        except:
            print("ping error")
        time.sleep(600)


async def handle(request):
    data = await request.json()
    await dp.feed_update(bot, data)
    return web.Response()

####запись и запуск бота
async def main():
    app = web.Application()
    app.router.add_post("/webhook", handle)
    await bot.set_webhook("https://my-telegram-bot-on3x.onrender.com/webhook")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    await asyncio.Event().wait()

    asyncio.create_task(alarms())



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"я спать пошла, спокойной ночи\n")