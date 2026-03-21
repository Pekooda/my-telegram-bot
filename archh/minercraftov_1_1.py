#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, logging, random, re, requests, sys, inspect, html, os, json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone, time
from dotenv import load_dotenv
from aiohttp import web


### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
PIXABAY_KEY = os.getenv("E_PIXABAY_KEY")
PEXELS_KEY = os.getenv("E_PEXELS_KEY")
REDDIT_KEY = os.getenv("E_REDDIT_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
JUNK_ID = int(os.getenv("E_JUNK_ID"), 0)
OT_ID = int(os.getenv("E_OT_ID"), 0)
COVINOC_ID = int(os.getenv("E_COVINOC_ID"), 0)
HURM_ID = int(os.getenv("E_HURM_ID"), 0)


### СТИКЕРПАКИ
RAND = {}
RANDSTICK_str = os.getenv("E_RANDSTICK", "{}")
RANDSTICK = json.loads(RANDSTICK_str)

### ПРИВЕТСТВИЯ
GREETINGS_str = os.getenv("E_GREETINGS", "[]")
GREETINGS = json.loads(GREETINGS_str)


### Я КИДАЮ МЕДИА
MURA_NIQ = os.getenv("E_MURA_NIQ")
CHEZ_NIQ = os.getenv("E_CHEZ_NIQ")
MAX_NIQ = os.getenv("E_MAX_NIQ")
LEAFY_NIQ = os.getenv("E_LEAFY_NIQ")
VSE_NIQ = os.getenv("E_VSE_NIQ")
VTRI_NIQ = os.getenv("E_VTRI_NIQ")
BEER_str = os.getenv("E_BEER", "[]")
BEER = json.loads(BEER_str)
WINE_str = os.getenv("E_WINE", "[]")
WINE = json.loads(WINE_str)
WATER_str = os.getenv("E_WATER", "[]")
WATER = json.loads(WATER_str)


### Я ВИЖУ МЕДИА
VORO_UIQ = os.getenv("E_VORO_UIQ")
VEI_UIQ = os.getenv("E_VEI_UIQ")
ADALI_UIQ = os.getenv("E_ADALI_UIQ")
SAD_UIQ_str = os.getenv("E_SAD_UIQ", "[]")
SAD_UIQ = json.loads(SAD_UIQ_str)
BAD_UIQ_str = os.getenv("E_BAD_UIQ", "[]")
BAD_UIQ = json.loads(BAD_UIQ_str)


### СТАНДАРТНЫЕ ПАРАМЕТРЫ
bot = Bot(
    token=TOKEN_KEY,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
TZ = timezone.utc
BOT_START = datetime.now(TZ)
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
bot_enabled = True


















#### КОМАНДЫ БОТА
### Начало жизни
async def start(message: types.Message, args: str):
    await message.answer("Я работаю.")


### ВОЗМОЖНО выдать админку
async def admin(message: types.Message, args: str):
    if random.random() < 0.0003619:
        await message.answer("Ты реально считаешь, что команда работает? =/")


### Пожелать доброго утра
async def gm(message: types.Message, args: str):
    await message.reply(random.choice(GREETINGS))


### Поставить лайк сообщению
async def like(message: types.Message, args: str):
    quer = message.text.split(maxsplit=1)
    query = quer[1].strip() if len(quer) > 1 else "👍"
    try:
        success = await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=(message.reply_to_message.message_id if message.reply_to_message is not None else message.message_id),
            reaction=[{"type": "emoji", "emoji": query}]
        )
    except Exception as e:
        return await message.reply("такой реакции нету в лайках")


### Отобрать лайк с сообщения
async def nolike(message: types.Message, args: str):
    if not message.reply_to_message:
        return await message.reply("укажи откуда убрать лайк плиз")
    success = await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
        reaction=[]
    )


### Гамбл игра 
## Параметризация
points_by_chat = defaultdict(lambda: defaultdict(int))
CUSTOM_STEPS = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
def format_cups(n: int) -> str:
    n_abs = abs(n)
    last_two = n_abs % 100
    last = n_abs % 10
    if 11 <= last_two <= 14:
        form = "кубков"
    else:
        if last == 1:
            form = "кубок"
        elif 2 <= last <= 4:
            form = "кубка"
        else:
            form = "кубков"
    return f"{n} {form}"

## Сама игра
async def necredit(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    change = random.choice(CUSTOM_STEPS)
    points_by_chat[chat_id][user_id] += change
    total = points_by_chat[chat_id][user_id]
    if change == 0:
        return await message.reply(
            f"🟡 Ничья!\n"
            f"Всего у вас {format_cups(total)}"
        )
    if change > 0:
        prefix = "🟢 Вы выиграли!\nНачислено "
        change_str = format_cups(change)
    else:
        prefix = "🔴 Вы проиграли!\nОтчислено "
        change_str = format_cups(abs(change))
    await message.reply(
        f"{prefix}{change_str}\n"
        f"Всего у вас {format_cups(total)}"
    )

## Узнать количество кубков
async def pointy(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    total = points_by_chat[chat_id][user_id]
    await message.reply(f"У вас сейчас {format_cups(total)}")


### Переключатели
## Параметризация
rich = {
    "lab": defaultdict(lambda: False),
    "oda": defaultdict(lambda: False),
    "eda": defaultdict(lambda: False),
    "sad": defaultdict(lambda: True)
}

## Рычаги
async def richagi(message: types.Message, args: str, cmd_name: str):
    if message.date < BOT_START:
        return
    global rich
    chat_id = message.chat.id
    cmd = rich[f"{cmd_name}"][chat_id]
    if cmd_name == ("eda" or "sad") and message.from_user.id == HURM_ID:
        return await message.reply("шарикзамаскировалиходиткакамогус")
    if message.chat.type == "private":
        nm = f"⚠️ Предупреждение: работа \"рычагов\" уникальна для каждего чата\n"
    else:
        nm = ""
    texting = (message.text or "").split(maxsplit=1)
    if len(texting) < 2:
        return await message.reply(f"{nm}Состояние {cmd_name}: {'🟢' if cmd else '🔴'} {cmd}\n\nЧтобы переключить режим, нужно вписать дополнительно \"on\" или \"off\"")
    text = str(texting[1])
    if text == "on" and cmd:
        return await message.reply(f"{nm}⚠️ Рычаг {cmd_name} уже включён")
    elif text == "on" and not cmd:
        rich[f"{cmd_name}"][chat_id] = True
        return await message.reply(f"{nm}✅ Рычаг {cmd_name} сменен на 🟢 True")
    elif text == "off" and not cmd:
        return await message.reply(f"{nm}⚠️ Рычаг {cmd_name} уже выключен")
    elif text == "off" and cmd:
        rich[f"{cmd_name}"][chat_id] = False
        return await message.reply(f"{nm}✅ Рычаг {cmd_name} сменен на 🔴 False")
    else:
        return await message.reply(f"{nm}Чтобы переключить режим, нужно вписать дополнительно \"on\" или \"off\"")


### Рандомные стикерпаки
## Параметризация
MAX_TRIES = 10
def format_menu_text(commands_map: dict) -> str:
    lines = [""]
    for cmd in commands_map.keys():
        lines.append(f"/{cmd}\n")
    return "".join(lines)

## Список доступных стикерпаков
async def wts(message: types.Message, args: str):
    menu_body = format_menu_text(RAND)
    html = (
        "Выбери конкретную тему:"
        + "<blockquote expandable>"
        + menu_body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        + "</blockquote>"
        + "Либо случайную тему: /rs"
    )
    await message.reply(html, parse_mode=ParseMode.HTML)

## Случайный стикер
async def rs(message: types.Message, args: str):
    topic = random.choice(list(RAND.keys()))
    pack = random.choice(RAND[topic])
    try:
        sticker_set = await bot.get_sticker_set(name=pack)
    except Exception as e:
        return await message.reply(f"БЕЗ СПАМА БЕЗ СПАМА!!!!")
    allowed = [s for s in sticker_set.stickers if s.file_unique_id not in BAD_UIQ]
    if not allowed:
        return await message.reply("во те на те стикеры в квадрате все стикеры с матюками")
    sticker = random.choice(allowed)
    await message.answer_sticker(sticker.file_id)


### Случайные картинки/видео
## Параметризация
DEFAULT = [""]

## Генератор случайных картинок №1
async def rp(message: types.Message, args: str):
    query = message.text.removeprefix("/rp").strip()
    if not query and message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT)
    params = {"key": PIXABAY_KEY, "q": query, "image_type": "photo", "safesearch": "true", "per_page": 200}
    try:
        resp = requests.get("https://pixabay.com/api/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        return await message.reply("сайт упал чорт их подрал (или не упал)")
    if not hits:
        return await message.reply("Я ничо не нашла эх блин")
    bad_tokens = ("ai", "neural", "generated", "ai-art", "ai_generated", "aiart")
    filtered = []
    for h in hits:
        tags = (h.get("tags") or "").lower()
        page = (h.get("pageURL") or "").lower()
        user = (h.get("user") or "").lower()
        combined = f"{tags} {page} {user}"
        if any(bt in combined for bt in bad_tokens):
            continue
        filtered.append(h)
    pool = filtered or hits
    choice = random.choice(pool)
    img_url = choice.get("largeImageURL") or choice.get("webformatURL") or choice.get("previewURL")
    await message.reply_photo(img_url)

## Генератор случайных видео №1
async def rv(message: types.Message, args: str):
    query = message.text.removeprefix("/rv").strip()
    if not query and message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT)
    params = {"key": PIXABAY_KEY, "q": query, "video_type": "all", "per_page": 199}
    try:
        resp = requests.get("https://pixabay.com/api/videos/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        return await message.reply("Сервер уронили, видео не будет =(")
    if not hits:
        return await message.reply("Я ничего не нашла эх блин")
    for _ in range(5):
        bad_tokens = ("ai", "neural", "generated", "ai-art", "ai_generated", "aiart")
        filtered = []
        for h in hits:
            tags = (h.get("tags") or "").lower()
            page = (h.get("pageURL") or "").lower()
            user = (h.get("user") or "").lower()
            combined = f"{tags} {page} {user}"
            if any(bt in combined for bt in bad_tokens):
                continue
            filtered.append(h)
        pool = filtered or hits
        choice = random.choice(pool)
        video_data = choice.get("videos", {})
        for quality in ["tiny", "small", "medium"]:
            url = video_data.get(quality, {}).get("url", "")
            if url:
                video_url = url.replace("http://", "https://")
                try:
                    return await message.reply_animation(video_url)
                except Exception:
                    pass
    await message.reply("Видео ДОЛЖНО было быть, но что-то пошло не так, как всегда")

## Генератор случайных картинок №2
async def rp1(message: types.Message, args: str):
    query = message.text.removeprefix("/rp1").strip()
    if not query and message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT)
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/v1/search", params=params, headers=key, timeout=5)
        data = resp.json()
        photos = data.get("photos", [])
    except Exception as e:
        return await message.reply(f"ошибка кританула: {e}")
    if not photos:
        return await message.reply("Я ничо не нашла эх блин")
    choice = random.choice(photos)
    img_url = choice["src"]["original"]
    await message.reply_photo(img_url)

## Генератор случайных видео №2
async def rv1(message: types.Message, args: str):
    query = message.text.removeprefix("/rv1").strip()
    if not query and message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT)
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/videos/search", params=params, headers=key, timeout=5)
        data = resp.json()
        videos = data.get("videos", [])
    except Exception as e:
        return await message.reply(f"ошибка кританула: {e}")
    if not videos:
        return await message.reply("Я ничего не нашла эх блин")
    choice = random.choice(videos)
    url = choice["video_files"][0]["link"]
    video_url = url.replace("http://", "https://")
    await message.reply_animation(video_url)


### Узнать айди/уникал айди медиа
## Параметризация
awaiting_id: dict[int, asyncio.Task] = {}
async def timeout_wait(user_id: int):
    await asyncio.sleep(300)
    if user_id in awaiting_id:
        awaiting_id.pop(user_id)
        try:
            await bot.send_message(user_id, "время вышло крч")
        except Exception:
            pass

## Команда
async def id(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Эту команду можно использовать лишь в ЛС")
    user_id = message.from_user.id
    if user_id in awaiting_id:
        awaiting_id[user_id].cancel()
    task = asyncio.create_task(timeout_wait(user_id))
    awaiting_id[user_id] = task
    await message.answer("давай, шли медию мне")

## Медиа
@dp.message(lambda message: message.from_user.id in awaiting_id, F.chat.type == "private")
async def handle_media_id(message: Message):
    user_id = message.from_user.id
    if message.sticker:
        file_id = message.sticker.file_id
        unique_id = message.sticker.file_unique_id
    elif message.animation:
        file_id = message.animation.file_id
        unique_id = message.animation.file_unique_id
    elif message.voice:
        file_id = message.voice.file_id
        unique_id = message.voice.file_unique_id
    elif message.photo:
        largest = message.photo[-1]
        file_id = largest.file_id
        unique_id = largest.file_unique_id
    else:
        task = awaiting_id.pop(user_id)
        task.cancel()
        return await message.answer("чот не то, всё сначало блин")
    task = awaiting_id.pop(user_id)
    task.cancel()
    await message.answer(
        f"<code>ID:</code> <code>{file_id}</code>\n"
        f"<code>UNIQUE_ID:</code> <code>{unique_id}</code>",
        parse_mode="HTML"
    )


















#### УДАЛЁННЫЕ КОМАНДЫ
### Раньше был ивент с ёлками, но ща уже не зима всё гг
async def farm(message: types.Message, args: str):
    return await message.reply("ивент с ёлками закончился блин счастливого лета ждём следующую зиму.")
async def elka(message: types.Message, args: str):
    return await message.reply("ивент с ёлками закончился блин счастливого лета ждём следующую зиму.")
async def sellelki(message: types.Message, args: str):
    return await message.reply("ивент с ёлками закончился блин счастливого лета ждём следующую зиму.")

















#### КОНСОЛЬНАЯ ХЕРНЯ
### Заставить бота ливнуть с чата
async def pokapoka(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("нет, ты не можешь")
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("эй а откуда")
    try:
        target_id = int(parts[1])
    except ValueError:
        return await message.reply("нет блин")
    try:
        ok = await bot.leave_chat(target_id)
        await message.reply("ура" if ok else "да блин не отпустили")
    except Exception as e:
        await message.reply(f"не хачу, патамушта {e}")


### Отправить текст через бота
async def text(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("нет, ты не можешь")
    texting = (message.text or "").split()
    if len(texting) < 3:
        return await message.reply(f"Нужен ТЕКСТ\n\nНадо что-то поменять в жизни")
    m = str(texting[1])
    val = {
        "!1": OT_ID, # ОТ
        "!2": COVINOC_ID, # КОВИНОК
        "!40": PEKO_ID # ПИКУДА
    }
    mes_id = str(val.get(m, m))
    try:
        num = float(mes_id)
    except ValueError:
        return await message.reply(f"Мне нужен АЙДИ: /text <ID> <text>\n\nЛибо вспоминай сокращения")
    texting = (message.text or "").split(maxsplit=2)
    d = str(texting[2])
    NAME = await bot.get_chat(mes_id)
    chat = NAME.title or NAME.full_name
    await bot.send_message(mes_id, d)
    return await message.reply(f"Я написала в [{chat}]: {d}")


### Добавить "Понтяно" к сообщению ответом
async def pontyano(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("команда находится в стадии ПОЧИНКИ и может быть использовано лишь Барменом")
    kartinka = Image.open('типуда.webp')
    okidoki = kartinka.convert("RGBA")
    textda = message.reply_to_message.text
    text = "понтяно"
    draw = ImageDraw.Draw(okidoki)
    x, y = okidoki.size
    lobster = ImageFont.truetype("Lobster.ttf", (x+y)/20)
    segoeui = ImageFont.truetype("segoeui.ttf", (x+y)/15)
    draw.text((x*0.5, y*0.40), textda, font=segoeui, anchor="mm", fill =(255, 255, 255))
    draw.text((x*0.5, y*0.90), text, font=lobster, anchor="mm", fill =(255, 255, 255))
    okidoki.save("ogogo.webp")
    await message.reply_document(document=types.FSInputFile("ogogo.webp"))


### Добавить текст к картинке ответом 
async def pont(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("команда находится в стадии ПОЧИНКИ и может быть использовано лишь Барменом")
    try:
        filfil = message.reply_to_message.photo[-1].file_id
        fileda = await bot.get_file(filfil)
        buffer = BytesIO()
        await bot.download_file(fileda.file_path, buffer)
        buffer.seek(0)
        kartinka = Image.open(buffer)
        okidoki = kartinka.convert("RGB")
        text = message.text.removeprefix("/pont").strip()
#        text = "понтяно"
        draw = ImageDraw.Draw(okidoki)
        rx, ry = okidoki.size
        lobster = ImageFont.truetype("Lobster.ttf", (rx+ry)/20)
        x = rx/2
        y = ry*0.92
        draw.text((x, y), text, font=lobster, anchor="mm", fill =(255, 255, 255))
        okidoki.save("ogogo.png")
        await message.reply_photo(photo=types.FSInputFile("ogogo.png"))
    except Exception as e:
        print(f"OSHIBKA: {e}")


### СОВЕРШЕННО СЕКРЕТНАЯ КОМАНДА - картинки из реддита
## Параметризация
def search_reddit_images(query: str, limit: int = 50) -> list[str]:
    headers = {"User-Agent": REDDIT_KEY}
    params  = {"q": query, "limit": limit, "include_over_18": "off", "sort": "relevance", "spoiler": "off"}
    url = "https://www.reddit.com/search.json"
    resp = requests.get(url, headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    posts = resp.json().get("data", {}).get("children", [])
    images = []
    for post in posts:
        data = post.get("data", {})
        if data.get("post_hint") == "image" and data.get("url"):
            images.append(data["url"])
    return images

## Команда
async def rr40(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("команда настолько секретная и опасная, что не рекомендуется для использования")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Введите текст: `/rr40 Текст`")
    query = parts[1]
    try:
        urls = search_reddit_images(query, limit=100)
    except Exception as e:
        return await message.reply("секретный сервак упал картинки не будет")
    if not urls:
        return await message.reply("я ничего не нашла эх блин")
    img_url = random.choice(urls)
    await message.reply_photo(img_url)


### Магазин, где можно потратить кубки. На самом деле ты получаешь пнг картинку товара и всё, да
## Параметризация
PRICES = {"beer":  10, "wine":  50, "water": 1,}
ITEM_NAMES = {"beer": "ПИВО", "wine": "ВИНО", "water": "ВОДУ"}

## Магазин
async def shop(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("команда находится в стадии ПОЧИНКИ и временно не работает.")
    if message.date < BOT_START:
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💧 Вода — 1 кубок", callback_data="buy:water")],
        [InlineKeyboardButton(text="🍺 Пиво — 10 кубков", callback_data="buy:beer")],
        [InlineKeyboardButton(text="🍷 Вино — 50 кубков", callback_data="buy:wine")],
    ])
    await message.answer("прошлый магазин закрылся, поэтому пишу с нового магазина, название не скажу, что желаете купить?", reply_markup=keyboard)

## Нажимание на кнопки
@dp.callback_query(F.data.startswith("buy:"))
async def buy_item(cb: CallbackQuery):
    chat_id = cb.message.chat.id
    user_id = cb.from_user.id
    username = cb.from_user.full_name
    _, item = cb.data.split(":", 1)
    item_name = ITEM_NAMES.get(item, item)
    cost = PRICES.get(item)
    if cost is None:
        return await cb.answer("ты как сюда нажал читер блин", show_alert=True)
    balance = points_by_chat[chat_id][user_id]
    if balance < cost:
        return await cb.answer(f"Недостаточно кубков ({format_cups(balance)})", show_alert=True)
    points_by_chat[chat_id][user_id] -= cost
    new_balance = points_by_chat[chat_id][user_id]
    if item == "beer":
        images = BEER
    elif item == "wine":
        images = WINE
    else:
        images = WATER
    if not isinstance(images, list) or not images:
        return await message.answer("мне не дали товар, эх товара не будет", show_alert=True)
    file_id = random.choice(images)
    await bot.send_photo(chat_id=chat_id, photo=file_id,
        caption=(f"{username} КУПИЛ {item_name} ЗА {format_cups(cost)}!\n"))



















#### РАБОТА БОТА
@dp.message()
async def vse(message: Message):
### ВКЛЮЧИТЬ/ВЫКЛЮЧИТЬ БОТА
    global bot_enabled
    if message.text:
        if message.date < BOT_START:
            pass
        if message.text.lower() == "иди спать, майнер крафтов":
            if not bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("не пойду я спать не хочу")
            bot_enabled = False
            return await message.reply("хорошо, иду спать, всем спокойного сна")
        if message.text.lower() == "просыпайся, майнер крафтов":
            if bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("не хочу я просыпаться не мешай мне спать")
            bot_enabled = True
            return await message.reply("доброго утра всем! 😀")
## Проверка на работу бота
    if not bot_enabled:
        return


### Информация
    global RANDSTICK, RAND
    chat_id = message.chat.id
    if message.chat.id != OT_ID:
        outout = ("monitor", "v", "fox", "voro", "leafy", "firey", "two", "dandy", "bobr", "pvz", "teto", "scampton", "bear", "bobr", "jimo", "pon", "skelet", "lomat", "cow")
        REALLYOUT = {k: RANDSTICK[k] for k in outout}
        RAND = REALLYOUT
    else: 
        RAND = RANDSTICK


### Мгновенная реакция
    if message.from_user.id == HURM_ID and rich["eda"][chat_id]:
        return await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if message.from_user.id == JUNK_ID and rich["oda"][chat_id]:
        await message.reply("*здесь злой текст о том, что Джанкил должен ~~отправится за игру в форсакен~~ отправиться кодить*")
    if message.from_user.id == HURM_ID and rich["sad"][chat_id]:
        if message.text.lower() == "😭" or message.text.lower() == "🥺":
            return await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if message.sticker.file_unique_id in SAD_UIQ:
            return await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


### ШАНСЫ
    if message.chat.id == OT_ID:
        if random.random() < 0.0003619: 
            await message.reply("СЛУЖЕБНОЕ СООБЩЕНИЕ")
        if random.random() < 0.00003619: 
            await message.reply("НАСТОЛЬКО СЛУЖЕБНОЕ СООБЩЕНИЕ, ЧТО ПИПЕЦ, 1 к 27630")
        if random.random() < 0.000003619: 
            await message.reply("ГИГАСЛУЖЕБНОЕ СООБЩЕНИЕ БОГОВ ОЛИМПУСА, 1 к 276300!!!!!")
        if random.random() < 0.01:
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[{"type": "emoji", "emoji": "👍"}]
            )
        if message.text and "все" in message.text.lower() and random.random() < 0.01:
            await message.reply_sticker(sticker=VSE_NIQ)


### КОНСОЛЬ
    chat = message.chat.title or message.from_user.full_name
    username = message.from_user.full_name
    emoji = getattr(message.sticker, "emoji", None)
    content = f"{emoji + ' ' if emoji else ''}{'[' + message.content_type.removeprefix("ContentType.") + '] ' if not message.text else ''}{message.caption or message.text if message.caption or message.text else ''}"
    print(f"[{chat}]\n{username}: {content}")


### РАБОТА КОМАНД
    if message.text and message.text.startswith("/"):
        parts = message.text.split(maxsplit=1)
        cmd_with_slash = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cmd = cmd_with_slash.lstrip("/").split("@", 1)[0].lower()
        if cmd in RAND:
            pack_list = RAND.get(cmd, [])
            if not pack_list:
                return await message.reply("Бармен не предоставил мне стикерпаков =/")
            chosen = random.choice(pack_list)
            sticker_set = await bot.get_sticker_set(name=chosen)
            allowed = [s for s in sticker_set.stickers if s.file_unique_id not in BAD_UIQ]
            if not allowed:
                return await message.reply("вот те на те все стикеры с матюками")
            sticker = random.choice(allowed)
            await message.answer_sticker(sticker.file_id)
        if cmd in rich:
            await richagi(message, args, cmd)
        else:
            func = getattr(sys.modules[__name__], cmd, None)
            if cmd == "richagi":
                return
            if func and inspect.iscoroutinefunction(func):
                await func(message, args)
        return


### БЛОК ВЕБХУКА
    if message.date < BOT_START:
        return


### ЗЕРКАЛО
    if rich["lab"][chat_id]:
        chat = message.chat.id
        if message.text:
            original = message.text.replace(".", ",")
            await bot.send_message(chat_id=chat, text=original)
        if message.photo:
            original = message.caption.replace(".", ",")
            media = message.photo[-1].file_id
            await bot.send_photo(chat_id=chat, photo=media, caption=original or None)
        if message.animation:
            original = message.caption.replace(".", ",")
            media = message.animation.file_id
            await bot.send_animation(chat_id=chat, animation=media, caption=original or None)
        if message.sticker:
            media = message.sticker.file_id
            await bot.send_sticker(chat_id=chat, sticker=media)
        if message.video:
            media = message.video.file_id
            await bot.send_video(chat_id=chat, video=media)


### Реакция на текст
## Реакция на полный текст
    if message.text:
        if message.text.lower() == "кейн, купи пиво":
            await message.answer("Кейн, купи пиво")
        if message.text.lower() == "я вернулся":
            await message.answer_sticker(sticker=MAX_NIQ)
        if message.text.lower() == "кобо":
            await message.answer("Справді гуманізований розумний голос")
        if message.text.lower() == "муравей":
            await message.reply_sticker(sticker=CHEZ_NIQ)
        if message.text.lower() == "че задали":
            await message.reply_sticker(sticker=MURA_NIQ)
        if message.text.lower() == "воро":
            await message.answer("Воро")
        if message.text.lower() == "2763":
            await message.reply_sticker(sticker=LEAFY_NIQ)
## Реакция на текст в сообщении
        if "майнера крафтов" in message.text.lower():
            await message.reply("не зли меня, бяка >=(")
## Реакция на стикеры
    if message.sticker:
        if message.sticker.file_unique_id == VORO_UIQ:
            await message.reply("Воро")
        if message.sticker.file_unique_id == VEI_UIQ:
            await message.reply_sticker(sticker=CHEZ_NIQ)
        if message.sticker.file_unique_id == ADALI_UIQ:
            await message.reply_sticker(sticker=MURA_NIQ)


















#### БУДИЛЬНИКИ
async def alarms():
### Параметризация
    global bot_enabled
    now = datetime.now(MSK)

### Сообщение админу о включении
    await bot.send_message(PEKO_ID, "доброе утро!")

### Сообщение чату о включении, если утро
    if 7 <= now.hour < 13:
        await bot.send_message(OT_ID, random.choice(GREETINGS))


### Сообщение о времени
    while True:
## Сообщение о 13:56
        if MSKnow.hour == 13 and MSKnow.minute == 56:
            await bot.send_photo(OT_ID, photo=VTRI_NIQ)
            await bot.send_photo(COVINOC_ID, photo=VTRI_NIQ)
            await asyncio.sleep(61)
        await asyncio.sleep(5)
## Сообщение о 19:52
        if MSKnow.hour == 19 and MSKnow.minute == 52:
            await bot.send_message(OT_ID, "📻📻📻")
            await asyncio.sleep(61)
        await asyncio.sleep(5)



















#### ТЕКСТ В КОМАНДНОЙ СТРОКЕ
#### ЗДЕСЬ АХУН ЗНАЕТ ЧО ПРОИСХОДИТ, НО ЧТО-ТО ПРОИСХОДИТ
#### МНЕ ЭТУ ФИГНЮ НЕЙРОСЕТЬ СГЕНЕРИЛА И ЧО С НЕЙ ДЕЛАТЬ ДА АЗ
class ChatFilter(BaseFilter):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id == self.chat_id
async def send_sticker(cmd: str):
    packs = RANDSTICK.get(cmd)
    if not packs:
        print(f"а? чо єто? {cmd}")
        return
    pack = random.choice(packs)
    set_ = await bot.get_sticker_set(pack)
    stickers = [s for s in set_.stickers if s.file_unique_id not in BAD_UIQ]
    if not stickers:
        print(f"У {pack} МАТЮЮЮЮЮЮЮЮЮЮЮЮК")
        return
    sticker = random.choice(stickers)
    await bot.send_sticker(OT_ID, sticker=sticker.file_id)
    print(f"Швирнула из {pack}")
async def console_sender():
    loop = asyncio.get_running_loop()
    print("тут длинный текст я сократила кароче")
    while True:
        try:
            line = await loop.run_in_executor(None, input, "> ")
        except (EOFError, KeyboardInterrupt):
            print("ЧОТА НА КИТАЙСКОМ ЧОТА НИПОНЯЛА")
            break
        if not line.strip():
            continue
        if line.startswith("/"):
            cmd = line[1:].split("@", 1)[0]
            await send_sticker(cmd)
        else:
            try:
                await bot.send_message(chat_id=OT_ID, text=line)
                print("Швирнула... а шо швирнула?")
            except Exception as e:
                print("не хочу отправлять вот Опричнина:", e)














WEBHOOK_PATH = "/tg_update"
WEBHOOK_SECRET = "telegkasecretnaya"
WEBHOOK_URL = f"https://my-telegram-bot-on3x.onrender.com{WEBHOOK_PATH}"

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

async def on_shutdown(app):
    await bot.delete_webhook()

####запись и запуск бота
#async def main():
app = web.Application()
SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=WEBHOOK_SECRET
).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 10000))
        web.run_app(app, host="0.0.0.0", port=port)
#        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"я спать пошла, спокойной ночи\n")