#### ВЕРСИИ:
# 1.0 - релиз бота
# 1.1 - фикс багов
# 1.2 - релиз создания стикерпаков
# 1.3 - шкала ярости и орлюки, поддержка базы данных, короче всё всё всё
# 1.3.wh - вебхук

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, logging, random, re, requests, sys, inspect, html, os, json, ffmpeg, subprocess, math, emoji, aiohttp
from aiohttp import web
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions, FSInputFile, Update
from aiogram.types.input_sticker import InputSticker
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.enums import ParseMode
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone, time
from dotenv import load_dotenv
from pilmoji import Pilmoji
from pilmoji.helpers import getsize


### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
URL_KEY = os.getenv("E_URL_KEY")
PIXABAY_KEY = os.getenv("E_PIXABAY_KEY")
PEXELS_KEY = os.getenv("E_PEXELS_KEY")
REDDIT_KEY = os.getenv("E_REDDIT_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
JUNK_ID = int(os.getenv("E_JUNK_ID"), 0)
OT_ID = int(os.getenv("E_OT_ID"), 0)
OTOLD_ID = int(os.getenv("E_OTOLD_ID"), 0)
COVINOC_ID = int(os.getenv("E_COVINOC_ID"), 0)
HURM_ID = int(os.getenv("E_HURM_ID"), 0)
TIM_ID = int(os.getenv("E_TIM_ID"), 0)
RANDSTICK = json.loads(os.getenv("E_RANDSTICK", "{}"))
GREETINGS = json.loads(os.getenv("E_GREETINGS", "[]"))
MURA_NIQ = os.getenv("E_MURA_NIQ")
CHEZ_NIQ = os.getenv("E_CHEZ_NIQ")
MAX_NIQ = os.getenv("E_MAX_NIQ")
LEAFY_NIQ = os.getenv("E_LEAFY_NIQ")
VSE_NIQ = os.getenv("E_VSE_NIQ")
VTRI_NIQ = os.getenv("E_VTRI_NIQ")
VORO_UIQ = os.getenv("E_VORO_UIQ")
CRO_UIQ = os.getenv("E_CRO_UIQ")
VEI_UIQ = os.getenv("E_VEI_UIQ")
ADALI_UIQ = os.getenv("E_ADALI_UIQ")
SAD_UIQ = json.loads(os.getenv("E_SAD_UIQ", "[]"))
BAD_UIQ = json.loads(os.getenv("E_BAD_UIQ", "[]"))
MC_NAME = json.loads(os.getenv("E_MC_NAME", "[]"))
MATUUUK = json.loads(os.getenv("E_MATUUUK", "[]"))
DEFAULT_QUERY = json.loads(os.getenv("E_DEFAULT_QUERY", '""'))
MC_RAGE = json.loads(os.getenv("E_MC_RAGE", '""'))
MC_OVERRAGE = json.loads(os.getenv("E_MC_OVERRAGE", '""'))
outout = tuple(json.loads(os.getenv("E_outout")))
MY_CHEST = os.getenv("E_MY_CHEST")




### ПЕРЕМЕННЫЕ
bot = Bot(token=TOKEN_KEY)
dp = Dispatcher()
TZ = timezone.utc
BOT_START = datetime.now(TZ)
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
bot_enabled = True
consolelog = True
RAND = {}
mediaidcheck = defaultdict(int)




### ДАТАБАЗА
def openchest():
    try:
        with open(MY_CHEST, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"эээ ну крч проблема: {e}")
def closechest(chest):
    with open(MY_CHEST, "w", encoding="utf-8") as f:
        json.dump(chest, f, ensure_ascii=False, indent=4)


def nozerolast(parts, numb):
    if len(parts) > numb:
        COUNT = int(parts[numb])
    else:
        return 1
    if COUNT < 1:
        return 0
    if not parts[numb].lstrip("-").isdigit():
        return 0
    return COUNT




























#### КОМАНДЫ БОТА
### Начало жизни
async def start(message: types.Message, args: str):
    rand = random.randint(0, 1000)
    await message.answer(f"Я работаю. Меня запустили в {MSKnow}. Число: {rand}")


### ВОЗМОЖНО выдать админку
async def admin(message: types.Message, args: str):
    if random.random() < 0.0003619:
        await message.answer("Ты реально считаешь, что команда работает? =/")


### Пожелать доброго утра
async def gm(message: types.Message, args: str):
    await message.reply(random.choice(GREETINGS))


### Детектор АЙДИ
async def id(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Эту команду можно использовать лишь в ЛС")
    user_id = message.from_user.id
    if mediaidcheck[user_id]:
        mediaidcheck[user_id] = False
        await message.answer("Отправка АЙДИ медиа отключена.")
    else:
        mediaidcheck[user_id] = True
        await message.answer("Отправка АЙДИ медиа включена. Чтобы отключить, пропишите /id ещё раз")


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
def shopcheck(message, user_id, chest):
    if f"{user_id}" not in chest["shop_items"]:
        chest["shop_items"][f"{user_id}"] = {}
    for tovar, key in chest["shop"]["buy"].items():
        if tovar not in chest["shop_items"][f"{user_id}"]:
            chest["shop_items"][f"{user_id}"][tovar] = 0
    return chest
def pointycheck(message, game, chest):
    date = datetime.now(MSK).day
    used = False
    user_id = message.from_user.id
    if f"{user_id}" not in chest["pointy"]:
        chest["pointy"][f"{user_id}"]["VALUE"] = 0
        chest["pointy"][f"{user_id}"]["DATE"] = 0
    if chest["pointy"][f"{user_id}"]["DATE"] == date:
        used = True
    if game:
        chest["pointy"][f"{user_id}"]["DATE"] = date
    return chest, used



mgcheck = defaultdict(bool)


async def mathgame(user_id: int):
    global mgcheck
    mgcheck[str(user_id)] = True
    d1 = random.randint(1, 100)
    d2 = random.randint(1, 100)
    dz = random.chouce("+", "-")
    de = str(d1) + dz + str(d2)
    desc = """
Математика!
В течении 10 секунд реши следующее уравнение:
{de}
"""
    for i in range(20):
        await asyncio.sleep(0.5)


async def mganswer():
    return

## Сама игра
async def chip(message: types.Message, args: str):
    return await message.reply(f"Команда находится в состоянии ПОЧИНКИ")
    chest = openchest()
    user_id = message.from_user.id
    chest, used = pointycheck(message, False, chest)
    if used:
        return await message.reply(f"Ты уже играл сегодня :/")
    right, done = asyncio.create_task(mathgame(message.chat.id))
    wait = await done
    return
    change = random.choice(chest["WINS"])
    chest["pointy"][f"{user_id}"]["VALUE"] += change
    if change > 0:
        prefix = f"🟢 Вы выиграли!\nНачислено кубков: {change}\n"
    elif change < 0:
        prefix = f"🔴 Вы проиграли!\nОтчислено кубков: {abs(change)}\n"
    else:
        prefix = f"🟡 Ничья!\n"
    await message.reply(
        f"{prefix}\n"
        f"Сейчас у вас кубков: {chest["pointy"][f"{user_id}"]["VALUE"]}"
    )
    chest, used = pointycheck(message, True, chest)
    closechest(chest)

## Узнать количество кубков
async def pointy(message: types.Message, args: str):
    return await message.reply(f"Команда находится в состоянии ПОЧИНКИ")
    chest = openchest()
    user_id = message.from_user.id
    pointycheck(message, False, chest)
    chest = shopcheck(message, user_id, chest)
    nanameme = []
    for tovar, value in chest["shop_items"][f"{user_id}"].items():
        if value == 0:
            continue
        veshi = f"""
{chest["shop"]["buy"][tovar]["name"]} - {value} шт.
"""
        nanameme.append(veshi)
    info = "".join(nanameme).strip()
    await message.reply(f"""
У вас сейчас кубков: {chest["pointy"][f"{user_id}"]["VALUE"]}
Приобретены такие товары:
{info}
""")
    closechest(chest)

## Магазин
async def shop(message: types.Message, args: str):
    return await message.reply(f"Команда находится в состоянии ПОЧИНКИ")
    user_id = message.from_user.id
    chest = openchest()
    parts = (message.text or "").split()
    chest = shopcheck(message, user_id, chest)
    if len(parts) < 2 or not chest["shop"][f"{parts[1]}"]:
        await message.reply("""
Я решила сделать полный ребрендинг магазина, и пока-что я продаю воздух.
Цена одного грамма воздуха - 1 кубок.
Чтобы купить воздух, напишите /shop buy air <кол-во>
""")
        return closechest(chest)
    if parts[1] == "buy":
        COUNT = nozerolast(parts, 3)
        if not COUNT:
            return await message.answer(f"Неа, я принимаю лишь натуральные значения =/")
        TYPE = parts[2]
        PRICE = chest["shop"]["buy"][f"{TYPE}"]["price"] * COUNT
        if PRICE > chest["pointy"][f"{user_id}"]:
            return await message.reply("""
У вас недостаточно кубков, чтобы приобрести этот продукт =(
""")
        chest["pointy"][f"{user_id}"]["VALUE"] -= PRICE
        VALUE = chest["shop"]["buy"][f"{TYPE}"]["value"] * COUNT
        chest["shop_items"][f"{user_id}"][TYPE] += VALUE
        await message.reply(f"""
Вы купили {chest["shop"]["buy"][f"{TYPE}"]["name"].lower()} в количестве {VALUE} шт. потратив {PRICE} кубков
Сейчас у вас {chest["shop_items"][f"{user_id}"][f"{TYPE}"]} ед. товара и {chest["pointy"][f"{user_id}"]["VALUE"]} кубков
""")
    closechest(chest)


### Рычаги
async def richagi(message: types.Message, args: str, cmd_name: str):
    if cmd_name == ("eda" or "sad") and message.from_user.id == HURM_ID:
        return await message.reply("Тибе низя. >=|")
    if cmd_name == "uda" and message.from_user.id != PEKO_ID:
        return await message.reply("Нэ")
    texting = (message.text or "").split()
    if message.from_user.id == PEKO_ID and len(texting) > 2 and texting[2].lstrip("-").isdigit():
        chat_id = int(texting[2])
    else:
        chat_id = message.chat.id
    chest = openchest()
    cmd = chest["rich"][f"{chat_id}"][f"{cmd_name}"]
    if len(texting) < 2:
        return await message.reply(f"Состояние {cmd_name}: {'🟢' if cmd else '🔴'} {cmd}\n\nЧтобы переключить режим, нужно вписать дополнительно \"on\" или \"off\"")
    else:
        text = str(texting[1])
        if text == "on" and cmd:
            await message.reply(f"⚠️ Рычаг {cmd_name} уже включён")
        elif text == "on" and not cmd:
            chest["rich"][f"{chat_id}"][f"{cmd_name}"] = True
            await message.reply(f"✅ Рычаг {cmd_name} сменен на 🟢 True")
        elif text == "off" and not cmd:
            await message.reply(f"⚠️ Рычаг {cmd_name} уже выключен")
        elif text == "off" and cmd:
            chest["rich"][f"{chat_id}"][f"{cmd_name}"] = False
            await message.reply(f"✅ Рычаг {cmd_name} сменен на 🔴 False")
        else:
            await message.reply(f"Чтобы переключить режим, нужно вписать дополнительно \"on\" или \"off\"")
    closechest(chest)


### Рандомные стикерпаки
## Список доступных стикерпаков
async def wts(message: types.Message, args: str):
    lines = [""]
    for cmd in RAND.keys():
        lines.append(f"/{cmd}\n")
    menubody = "<blockquote expandable>" + "".join(lines) + "</blockquote>"
    await message.reply(f"""
Выбери конкретную тему:
{menubody}Либо случайную тему: /rs
""", parse_mode="HTML")

## Случайный стикер
async def rs(message: types.Message, args: str):
    if message.chat.id != OT_ID:
        REALLYOUT = {k: RANDSTICK[k] for k in outout}
        RAND = REALLYOUT
    else: 
        RAND = RANDSTICK
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


##########
def rage_meter(rage_level, rage_type):
    for key, label in rage_type.items():
        if "//" in key:
            start, end = key.split("//")
            if int(start) <= rage_level <= int(end):
                return label
        else:
            if int(key) == rage_level:
                return label
    return None

### Сменить количество ярости 
async def pong(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.answer(f"простиии, но ты не можешь...")
    set = False
    if args.startswith("!"):
        args = args.lstrip("!")
        set = True
    if not args.isdigit():
        return await message.answer(f"мне надо циферка...")
    chest = openchest()
    if set:
        chest["NUMB"] = int(args)
    else:
        chest["NUMB"] += int(args)
    closechest(chest)
    await message.answer(f"Моя злость теперь составляет: {chest["NUMB"]}")

## Снять гнев
async def mercy(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.answer(f"Тебе низя")
    chest = openchest()
    for key in chest["kazn"]:
        chest["kazn"][key]["NOW"] = 0
    closechest(chest)
    await message.answer(f"Хорошо, я его пощадила... но...")

## Покупка гнева
async def gnev(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.answer(f"простиии, но ты не можешь...")
    if message.chat.id != OT_ID and message.from_user.id != PEKO_ID:
        return await message.answer(f"Вот давай не в крысу, мой гнев выливать лишь публично")
    chat_id = message.chat.id
    parts = (message.text or "").split()
    OVERRAGE = 0
    chest = openchest()
    for key in chest["kazn"].values():
        OVERRAGE += key.get("NOW", 0)
    RAGE = html.escape(rage_meter(chest["NUMB"] + OVERRAGE, MC_RAGE))
    POVERRAGE = html.escape(rage_meter(OVERRAGE, MC_OVERRAGE))
    if len(parts) < 2:
        nanameme = []
        for subname, key in chest["kazn"].items():
            template = f"""
{"🟢" if key.get("NOW", 0) else "⚪️"} {key.get("NAME", "НЕТУ ИМЕНИ")} - {key.get("INFO", "НЕТУ ОПИСАНИЯ")}
{"Количество доступных применений" if key.get("TYPE", 0) == "use" else "Текущее время действия"}: {key.get("NOW", "???")} {"минут" if key.get("TYPE", 0) == "time" else ""}
Сила моего гнева, чтобы использовать: {key.get("PRICE", "???")}
Чтобы использовать, пропишите <code>/gnev {subname}</code>"""
            nanameme.append(template)
        info = "<blockquote expandable>" + "".join(nanameme).strip() + "</blockquote>"
        return await message.answer(f"""
Текущая сила моего гнева: {chest["NUMB"]}
<b>{RAGE}{POVERRAGE}</b>
Список моего гнева:
{info}
Чтобы купить несколько товаров, в конце припишите количество
""", parse_mode="HTML")
    id = str(parts[1])
    if not parts[1] in chest["kazn"].keys():
        return await message.answer(f"Такой гнев я не преподаю :/")
    COUNT = nozerolast(parts, 2)
    if not COUNT:
        return await message.answer(f"Неа, я принимаю лишь натуральные значения =/")
    n = chest["kazn"][id]["NAME"]
    p = chest["kazn"][id]["PRICE"] * COUNT
    v = chest["kazn"][id]["VALUE"] * COUNT
    if chest["NUMB"] < p:
        return await bot.send_message(chat_id, f"Недостаточно моего гнева!\nСила моего гнева, которую нужно приложить, чтобы использовать этот гнев: {p}\nТекущая сила моего гнева: {chest["NUMB"]}")
    chest["NUMB"] -= p
    chest["kazn"][id]["NOW"] += v
    await bot.send_message(chat_id, f"""
{n} теперь используется!
{"Количество сообщений, которые будут удаляться: " + str(chest["kazn"][id]["NOW"]) if id == "ob" else "Время действия этого гнева: " + str(chest["kazn"][id]["NOW"]) + " минут"}
Текущая сила моего гнева: {chest["NUMB"]}
""")
    return closechest(chest)


### Случайные картинки/видео
## Параметризация
def MATUK_CHECK(text):
    for w in MATUUUK:
        pattern = rf"^{re.escape(w)}\w*"
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False

## Рандом на "орлюк"
async def orluk(message: types.Message, args: str):
    query = "орел"
    tes = random.choice([rv, rv1, rp, rp1])
    eagle = await tes(message, query)
    if tes in (rp, rp1):
        await message.answer_photo(eagle)
    else:
        await message.answer_animation(eagle)

def queryfilter(message, query, com):
    R = message.text.startswith(f"/{com}")
    if message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT_QUERY)
    return R, query

## Генератор случайных картинок №1
async def rp(message: types.Message, query: str):
    RP, query = queryfilter(message, query, "rp")
    params = {"key": PIXABAY_KEY, "q": query, "image_type": "photo", "safesearch": "true", "per_page": 200}
    try:
        resp = requests.get("https://pixabay.com/api/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        if RP:
            return await message.reply(f"ошибка кританула: {e}")
        else:
            return "no"
    if not hits:
        if RP:
            return await message.reply("Я ничего не нашла эх блин")
        else:
            return "no"
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
    img_url = choice.get("webformatURL")
    if RP:
        await message.answer_photo(img_url)
    else:
        return img_url

## Генератор случайных видео №1
async def rv(message: types.Message, query: str):
    RV, query = queryfilter(message, query, "rv")
    params = {"key": PIXABAY_KEY, "q": query, "video_type": "all", "per_page": 199}
    try:
        resp = requests.get("https://pixabay.com/api/videos/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        if RV:
            return await message.reply(f"ошибка кританула: {e}")
        else:
            return "no"
    if not hits:
        if RV:
            return await message.reply("Я ничего не нашла эх блин")
        else:
            return "no"
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
            if RV:
                return await message.answer_animation(video_url)
            else:
                return video_url

## Генератор случайных картинок №2
async def rp1(message: types.Message, query: str):
    RP1, query = queryfilter(message, query, "rp1")
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/v1/search", params=params, headers=key, timeout=5)
        data = resp.json()
        photos = data.get("photos", [])
    except Exception as e:
        if RP1:
            return await message.reply("ошибка кританула: {e}")
        else:
            return "no"
    if not photos:
        if RP1:
            return await message.reply(f"Я ничего не нашла эх блин")
        else:
            return "no"
    choice = random.choice(photos)
    img_url = choice["src"]["large"]
    if RP1:
        await message.answer_photo(img_url)
    else:
        return img_url

## Генератор случайных видео №2
async def rv1(message: types.Message, query: str):
    RV1, query = queryfilter(message, query, "rv1")
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/videos/search", params=params, headers=key, timeout=5)
        data = resp.json()
        videos = data.get("videos", [])
    except Exception as e:
        if RV1:
            return await message.reply(f"ошибка кританула: {e}")
        else:
            return "no"
    if not videos:
        if RV1:
            return await message.reply("Я ничего не нашла эх блин")
        else:
            return "no"
    choice = random.choice(videos)
    url = choice["video_files"][0]["link"]
    video_url = url.replace("http://", "https://")
    if RV1:
        await message.answer_animation(video_url)
    else:
        return video_url


### Сделать что-то со стикерпаком
msp = defaultdict(str)
nsp = defaultdict(str)
ssp = defaultdict(str)
amsp = defaultdict(str)
assp = defaultdict(str)
input_path = "input.mp4"
output_path = "output.webm"
CREATIV: dict[int, asyncio.Task] = {}
async def timeout_wait(user_id: int):
    await asyncio.sleep(300)
    if user_id in CREATIV:
        CREATIV.pop(user_id)
        try:
            await bot.send_message(user_id, "время вышло крч")
        except Exception:
            pass

ADDIN: dict[int, asyncio.Task] = {}
async def timeout_wait(user_id: int):
    await asyncio.sleep(300)
    if user_id in ADDIN:
        ADDIN.pop(user_id)
        try:
            await bot.send_message(user_id, "время вышло крч")
        except Exception:
            pass

def gduration(path):
    process = subprocess.run(
        ["ffprobe", "-hide_banner", "-loglevel", "quiet", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True,
        text=True
    )
    if not process.stdout.strip():
        raise Exception(f"FFprobe failed: {process.stderr}")
    return float(process.stdout.strip())
def convert_to_sticker(input_path, output_path):
    duration = gduration(input_path)
    filters = "scale=512:512"
    if duration > 2.95:
        speed = duration / 2.95
        filters += f",setpts=PTS/{speed}"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "quiet", "-y", "-i", input_path, "-vf", filters, "-an", "-c:v", "libvpx-vp9", "-b:v", "350k", "-c:a", "libopus", "-b:a", "32k", "-t", "2.95", output_path
    ])
## Команда
async def asp(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Эту команду можно использовать лишь в ЛС")
    user_id = message.from_user.id
    global assp, amsp
    texting = (message.text or "").split()
    if len(texting) < 2:
        return await message.reply(f"Надо написать так:\n\n/asp <ID>\n\n<ID> писать без <_by_minercraftov_bot> в конце, это я сама допишу, оки?\nИ заметь, я тупая, я не запоминаю какие вы там айдишки мне кидали, так что не кричи на меня, если я скажу, что стикерпак не создаётся, оки?\nПредупреждаю: Вы можете добавить стикер лишь к своему стикерпаку, который был создан с помощью /csp, в ином случае выдаст ошибку")
    assp[user_id] = str(texting[1])
    val = {
        "!1": "blablalablala40", # Da blin
        "!40": "gifgif" # Простогифки
    }
    assp[user_id] = str(val.get(assp[user_id], assp[user_id]))
    amsp[user_id] = assp[user_id] + "_by_MinerCraftov_Bot"
    if len(amsp[user_id]) > 64 or not re.fullmatch(r"[A-Za-z0-9_]+", amsp[user_id]) or "__" in amsp[user_id] or not amsp[user_id][0].isalpha():
        return await message.reply("Неправильное название айдишки.")
    if user_id in CREATIV:
        CREATIV[user_id].cancel()
    task = asyncio.create_task(timeout_wait(user_id))
    CREATIV[user_id] = task
    await message.answer("давай, шли видео мне. Предупреждаю: Вы можете добавить стикер лишь к своему стикерпаку, который был создан с помощью /csp, в ином случае выдаст ошибку")
## Медиа
@dp.message(lambda message: message.from_user.id in CREATIV, F.chat.type == "private")
async def hahaha(message: Message):
    user_id = message.from_user.id
    if message.video or message.animation:
        if message.video and message.video.file_size and message.video.file_size > 20*1024*1024:
            await message.reply("Слишком большая колбаса")
            pass
        if message.animation and message.animation.file_size and message.animation.file_size > 20*1024*1024:
            await message.reply("Слишком большая колбаса")
            pass
        try:
            await bot.download(
                message.video or message.animation,
                destination=input_path
            )
            convert_to_sticker(input_path, output_path)
            input_sticker = InputSticker(
                sticker=FSInputFile(output_path),
                format="video",
                emoji_list=["🍺"]
            )
            print(amsp)
            await bot.add_sticker_to_set(
                user_id=user_id,
                name=amsp[user_id],
                sticker=input_sticker
            )
            await message.reply(f"Стикер был добавлен в\nhttps://t.me/addstickers/{amsp[user_id]}")
            await bot.send_message(PEKO_ID, f"мужик по имени {message.from_user.full_name} швирнул стикер в стикерпак {amsp[user_id]}")
        except Exception as e:
            await message.answer(f"Ошибочка: {e}\n\nПридётся повторить создание снова")
            pass
    else:
        task = CREATIV.pop(user_id)
        task.cancel()
        await message.answer("чот не то, всё сначало блин")
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        return
    task = CREATIV.pop(user_id)
    task.cancel()
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        return


##СОЗДАТЬ СТИКЕРПАК
async def csp(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Эту команду можно использовать лишь в ЛС")
    user_id = message.from_user.id
    global msp, nsp, ssp
    texting = (message.text or "").split()
    if len(texting) < 3:
        return await message.reply(f"Надо написать так:\n\n/csp <ID> <NAME>\n\n<ID> писать без <_by_minercraftov_bot> в конце, это я сама допишу, оки?\nИ заметь, я тупая, я не запоминаю какие вы там айдишки мне кидали, так что не кричи на меня, если я скажу, что стикерпак не создаётся, оки?")
    texting = (message.text or "").split(maxsplit=2)
    ssp[user_id] = str(texting[1])
    msp[user_id] = ssp[user_id] + "_by_MinerCraftov_Bot"
    nsp[user_id] = str(texting[2])
    if len(msp[user_id]) > 64:
        return await message.reply("Слишком длинный ID, выбери короче, пожалуйста")
    if not re.fullmatch(r"[A-Za-z0-9_]+", msp[user_id]):
        return await message.reply("Прости, но я не принимаю такие литеры в айдишке стикерпака =/")
    if "__" in msp[user_id]:
        return await message.reply("Не ставь мне <__> в айдишке, телеграм не любит такое =(")
    if not msp[user_id][0].isalpha():
        return await message.reply("Пожалуйста не ставь циферки в начале айдишки, они страшные т_т")
    if len(nsp[user_id]) > 64:
        return await message.reply("Слишком длинное название (NAME), выбери короче, пожалуйста")
    if user_id in ADDIN:
        ADDIN[user_id].cancel()
    task = asyncio.create_task(timeout_wait(user_id))
    ADDIN[user_id] = task
    await message.answer(f"Пришли мне любое видео, что-бы я могла создать стикерпак. Предупреждаю: Айди стикерпака может быть занято и выдать ошибку. Айди стикерпака будет:\n\n{msp[user_id]}\n\nА название:\n\n{nsp[user_id]}\n\nЕсли чот не то - напиши чо-нибудь, чтобы я прекратила создание стикерпака")
@dp.message(lambda message: message.from_user.id in ADDIN, F.chat.type == "private")
async def hahaha(message: Message):
    user_id = message.from_user.id
    if message.video or message.animation:
        if message.video and message.video.file_size and message.video.file_size > 20*1024*1024:
            await message.reply("Слишком большая колбаса. Повторите команду /csp ещё раз, но с меньшим видео")
            pass
        if message.animation and message.animation.file_size and message.animation.file_size > 20*1024*1024:
            await message.reply("Слишком большая колбаса. Повторите команду /csp ещё раз, но с меньшим видео")
            pass
        try:
            await bot.download(
                message.video or message.animation,
                destination=input_path
            )
            convert_to_sticker(input_path, output_path)
            input_sticker = InputSticker(
                sticker=FSInputFile(output_path),
                format="video",
                emoji_list=["🍺"]
            )
            await bot.create_new_sticker_set(
                user_id=user_id,
                name=msp[user_id],
                title=nsp[user_id],
                stickers=[input_sticker]
            )
            await message.reply(f"Стикерпак был создан:\nhttps://t.me/addstickers/{msp[user_id]}\n\nСпасибо за внимание. Если нужон добавить стикер в стикерпак: пропиши /sp {ssp[user_id]} и добавляй дальше")
            await bot.send_message(PEKO_ID, f"мужик по имени {message.from_user.full_name} создал стикерпак <{nsp[user_id]}> с айдишкой <{msp[user_id]}>")
        except Exception as e:
            await message.answer(f"Ошибочка: {e}\n\nПридётся повторить создание снова")
            pass
    else:
        task = ADDIN.pop(user_id)
        task.cancel()
        await message.answer("чот не то, всё сначало блин")
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        return
    task = ADDIN.pop(user_id)
    task.cancel()
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        return


### ПОНТЯНО И ТЕКСТ
def textstab(x, y, text, maxlet, maxwid, maxsize, font, minsize):
    maxlet = math.floor(maxlet)
    n = 0
    pon = ""
    everyword = text.split()
    while n < len(everyword) and len(pon) + len(everyword[n]) + 1 < maxlet:
        pon += f"{everyword[n]} "
        n += 1
    try:
        if len(pon) <= maxlet*0.5:
            pon += everyword[n][:(maxlet-len(pon))]
        if len(pon) + len(everyword[n]) >= maxlet:
            pon = pon.strip()
            pon += "..."
    except Exception as e:
        pass
    pon = pon.strip()
    while maxsize > minsize:
        test = ImageFont.truetype(font, maxsize)
        width, heigh = getsize(pon, test)
        if width <= maxwid:
            break
        maxsize -= 1
    imfont = ImageFont.truetype(font, maxsize)
    return pon, imfont, maxsize

def addoutline(x, y, template, font, text, off, anch, ef):
    shadowColor = (0, 0, 0)
    with Pilmoji(template) as d:
    #move right
        d.text((x-off, y), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #move left
        d.text((x+off, y), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #move up
        d.text((x, y+off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #move down
        d.text((x, y-off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #diagnal left up
        d.text((x-off, y+off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #diagnal right up
        d.text((x+off, y+off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #diagnal left down
        d.text((x-off, y-off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    #diagnal right down
        d.text((x+off, y-off), text, font=font, anchor=anch, fill=shadowColor, emoji_position_offset=ef)
    return d

def emojionly(text, x, y):
    if all(char in emoji.EMOJI_DATA for char in text):
        return (0, -y*(0.09*x/y))
    else:
        return (0, -y*(0.015*x/y))

## Добавить "Понтяно" к сообщению
async def pont(message: types.Message, args: str):
    if message.reply_to_message and message.reply_to_message.caption:
        text = message.reply_to_message.caption.split("\n")
        user_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.full_name
    elif message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text.split("\n")
        user_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.full_name
    elif message.text or message.caption:
        text = args.split("\n")
        user_id = message.from_user.id
        name = message.from_user.full_name
    else:
        return await message.reply(f"я могу реагировать лишь на текст >_<")
    if random.random() < 0.99:
        pontyano = "понтяно"
    else:
        pontyano = "непонтяно"
    photo_id = await message.bot.get_user_profile_photos(user_id, limit=1)
    if photo_id.total_count > 0:
        template = Image.open('mestemplate.webp').convert("RGBA")
        file_id = photo_id.photos[0][-1].file_id
        file = await bot.get_file(file_id)
        buffer = BytesIO()
        await bot.download_file(file.file_path, buffer)
        buffer.seek(0)
        x, y = template.size
        coord = (x*0.2763, y*0.525)
        coord1 = (x*0.2763, y*0.325)
        mlt = 27
        mwt = x*0.6
        mln = 27
        mwn = x*0.6
        ava = Image.open(buffer)
        ava = ava.convert('RGBA')
        mask = Image.open("mask.png").convert('L')
        making = ImageOps.fit(ava, mask.size, centering=(0.5, 0.5))
        making.putalpha(mask)
        template.paste(making, (20, 85), mask=making)
        anch = "lm"
    else:
        template = Image.open('mestemplate1.webp').convert("RGBA")
        x, y = template.size
        coord = (x*0.5, y*0.525)
        coord1 = (x*0.5, y*0.325)
        mlt = 40
        mwt = x*0.8
        mln = 40
        mwn = x*0.8
        anch = "mm"
    mainpont = ImageFont.truetype("Lobster.ttf", (x+y)/20)
    textik = text[0]
    fontt = "segoeui.ttf"
    sizet = x/15
    min = x/30
    textot, imfontot, sizeot = textstab(x, y, textik, mlt, mwt, sizet, fontt, min)
    emojiofft = emojionly(textot, x, y)
    fontn = "segoeuibold.ttf"
    texton, imfonton, sizeon = textstab(x, y, name, mln, mwn, sizet, fontn, min)
    emojioffn = emojionly(texton, x, y)
    emojioffp = emojionly(pontyano, x, y)
    with Pilmoji(template) as d:
        d.text(coord, textot, font=imfontot, anchor=anch, fill =(255, 255, 255), emoji_position_offset=emojiofft)
        d.text(coord1, texton, font=imfonton, anchor=anch, fill =(255, 255, 255), emoji_position_offset=emojioffn)
        d.text((x*0.5, y*0.90), pontyano, font=mainpont, anchor="mm", fill =(255, 255, 255), emoji_position_offset=emojioffp)
    pont = "pont.webp"
    template.save(pont)
    await message.reply_sticker(sticker=types.FSInputFile(pont))
    os.remove(pont)


### Добавить текст к картинке ответом 
async def ttp(message: types.Message, args: str):
    buffer = BytesIO()
    if message.reply_to_message and message.reply_to_message.photo:
        pic_id = message.reply_to_message.photo[-1].file_id
        pic = await bot.get_file(pic_id)
        await bot.download_file(pic.file_path, buffer)
    elif message.photo:
        pic_id = message.photo[-1].file_id
        pic = await bot.get_file(pic_id)
        await bot.download_file(pic.file_path, buffer)
    elif message.reply_to_message and message.reply_to_message.sticker:
        pic_id = message.reply_to_message.sticker.file_id
        forma = "webp"
        pic = await bot.get_file(pic_id)
        await bot.download_file(pic.file_path, buffer)
    elif message.reply_to_message and message.reply_to_message.animation:
        pic_id = message.reply_to_message.animation.file_id
        forma = "png"
        pic = await bot.get_file(pic_id)
        await bot.download_file(pic.file_path, buffer)
    else:
        if not args:
            if message.reply_to_message and message.reply_to_message.text:
                args = message.reply_to_message.text
            elif message.reply_to_message and message.reply_to_message.caption:
                args = message.reply_to_message.caption
            if not args:
                args = random.choice(DEFAULT_QUERY)
        pic = await rp(message, args)
        if pic == "no":
            pic = await rp1(message, args)
        if pic == "no":
            return await message.reply(f"я ничо в rp/rp1 не нашла эх блин")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(pic) as r:
                    buffer = BytesIO(await r.read()) 
        except Exception as e:
            return await message.reply(f"что-то сломалось...")
    buffer.seek(0)
    if message.reply_to_message and ((message.reply_to_message.sticker and (message.reply_to_message.sticker.is_video or message.reply_to_message.sticker.is_animated)) or message.reply_to_message.animation):
        ohno = subprocess.run(
            ["ffmpeg", "-i", "pipe:0", "-frames:v", "1", "-f", "image2pipe", "-vcodec", forma, "pipe:1"],
            input=buffer.read(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        buffer = BytesIO(ohno.stdout)
        buffer.seek(0)
    dpic = Image.open(buffer).convert('RGBA')
    x, y = dpic.size
    font = "Lobster.ttf"
    size = x/10
    coord = (x*0.5, y*0.95)
    if message.reply_to_message and message.reply_to_message.sticker:
        mlt = 20*(x/y)
    else:
        mlt = 80*(x/y)
    mwt = x*0.9
    mina = x/100
    textout, fontout, sizeout = textstab(x, y, args.lower(), mlt, mwt, size, font, mina)
    if math.sqrt(x*y) > min(x, y):
        bal = min(x, y)
    else:
        bal = math.sqrt(x*y)
    off = bal/200
    emojioff = emojionly(textout, x, y)
    anch = "ms"
    templa = addoutline(coord[0], coord[1], dpic, fontout, textout, off, anch, emojioff)
    with Pilmoji(dpic) as pilmoji:
        pilmoji.text(coord, textout, font=fontout, anchor=anch, fill =(255, 255, 255), emoji_position_offset=emojioff)
    if message.reply_to_message and message.reply_to_message.sticker:
        ttps = "ttps.webp"
        dpic.save(ttps)
        await message.reply_sticker(sticker=types.FSInputFile(ttps))
        os.remove(ttps)
    else:
        ttp = "ttp.png"
        dpic.save(ttp)
        await message.reply_photo(photo=types.FSInputFile(ttp))
        os.remove(ttp)














#### КОНСОЛЬНАЯ ХЕРНЯ
### Заставить бота ливнуть с чата
async def pokapoka(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("нет, ты не можешь")
    if not args:
        return await message.reply("эй а откуда ливать")
    if args.startswith("-100"):
        leaveid = int(args)
        try:
            await bot.leave_chat(leaveid)
            return await message.reply("ура я ливнула")
        except Exception as e:
            return await message.reply("меня там нету ты чо")
    await message.reply("это ж даже не чат >_<")


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
        "!11": OTOLD_ID, # ОТ_OLD
        "!40": PEKO_ID # ПИКУДА
    }
    mes_id = str(val.get(m, m))
    if not mes_id.lstrip("-").isdigit():
        return await message.reply(f"Мне нужен АЙДИ: /text <ID> <text>\n\nЛибо вспоминай сокращения")
    texting = (message.text or "").split(maxsplit=2)
    d = str(texting[2])
    try:
        NAME = await bot.get_chat(mes_id)
        chat = NAME.title or NAME.full_name
        await bot.send_message(mes_id, d)
        await message.reply(f"Я написала в [{chat}]: {d}")
    except Exception as e:
        await message.reply(f"Меня там даже нету ты чо")


### СОВЕРШЕННО СЕКРЕТНАЯ КОМАНДА - картинки из реддита
async def rr40(message: types.Message, query: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("команда настолько секретная и опасная, что не рекомендуется для использования")
    RR40, query = queryfilter(message, query)
    headers = {"User-Agent": REDDIT_KEY}
    params  = {"q": query, "limit": 100, "include_over_18": "off", "sort": "relevance", "spoiler": "off"}
    url = "https://www.reddit.com/search.json"
    urls = []
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        posts = resp.json().get("data", {}).get("children", [])
        for post in posts:
            data = post.get("data", {})
            if data.get("post_hint") == "image" and data.get("url"):
                urls.append(data["url"])
    except Exception as e:
        return await message.reply("секретный сервак упал картинки не будет")
    if not urls:
        return await message.reply("я ничего не нашла эх блин")
    img_url = random.choice(urls)
    await message.reply_photo(img_url)




















#### РАБОТА БОТА
@dp.message()
async def vse(message: Message):
### ВКЛЮЧИТЬ/ВЫКЛЮЧИТЬ БОТА
    if not message.date < BOT_START and message.text and message.text.lower().startswith("майнер крафтов, "):
        global bot_enabled
        if message.text.lower() == "майнер крафтов, спать":
            if not bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("не пойду я спать не хочу")
            bot_enabled = False
            return await message.reply("хорошо, иду спать, всем спокойного сна")
        elif message.text.lower() == "майнер крафтов, проснуться":
            if bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("не хочу я просыпаться не мешай мне спать")
            bot_enabled = True
            return await message.reply("доброго утра всем! 😀")
    if message.text and message.text.startswith("/em"):
        chest = openchest()
        parts = message.text.lower().removeprefix("/em").strip().split()
        YES = parts[0]
        EMER = chest["rich"]["5513644023"].keys()
        args = ""
        if YES in EMER:
            await richagi(message, args, YES)
        if YES == "mercy":
            await mercy(message, args)
        chest = openchest()
### Проверка на работу бота, открыть датабазу
    if not bot_enabled:
        return
    chest = openchest()
    chat_id = message.chat.id
    user_id = message.from_user.id
### АНТИ-СПАМ
    if not message.date < BOT_START and message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["sad"] and ((message.text and message.text in ("😭", "🥺")) or (message.sticker and message.sticker.file_unique_id in SAD_UIQ)):
        return await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


### ШАНСЫ
    if message.chat.id == OT_ID and random.random() < 0.0003619: 
        if random.random() < 0.01:
            await message.reply("ГИГАСЛУЖЕБНОЕ СООБЩЕНИЕ БОГОВ ОЛИМПУСА, 1 к 276300!!!!!")
        elif random.random() < 0.1: 
            await message.reply("НАСТОЛЬКО СЛУЖЕБНОЕ СООБЩЕНИЕ, ЧТО ПИПЕЦ, 1 к 27630")
        else:
            await message.reply("СЛУЖЕБНОЕ СООБЩЕНИЕ")


### КОНСОЛЬ
    if consolelog:
        chat = message.chat.title or message.from_user.full_name
        username = message.from_user.full_name
        emoji = getattr(message.sticker, "emoji", None)
        content = f"{emoji + ' ' if emoji else ''}{'[' + message.content_type.removeprefix("ContentType.") + '] ' if not message.text else ''}{message.caption or message.text if message.caption or message.text else ''}"
        print(f"[{chat}]\n{username}: {content}")



### ВСЁ, ЧТО НИЖЕ - НЕ ОТПРАВИТСЯ ПРИ ЗАПУСКЕ
    if message.date < BOT_START:
        return
### Мгновенная реакция
    if message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["eda"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.from_user.id == TIM_ID and chest["rich"][f"{chat_id}"]["uda"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.from_user.id == JUNK_ID and chest["rich"][f"{chat_id}"]["oda"]:
        await message.reply("*здесь злой текст о том, что Джанкил должен ~~отправится за игру в форсакен~~ отправиться кодить*")


### ЗАПИСЬ ЧАТА В ДЖСОН
    if f"{chat_id}" not in chest["rich"]:
        chest["rich"][f"{chat_id}"] = {
            "lab": False,
            "oda": False,
            "eda": False,
            "uda": False,
            "sad": True
        }
        closechest(chest)

### РАБОТА КОМАНД
    if (message.text and message.text.startswith("/")) or (message.caption and message.caption.startswith("/")):
        global RAND
        if message.chat.id != OT_ID:
            REALLYOUT = {k: RANDSTICK[k] for k in outout}
            RAND = REALLYOUT
        else: 
            RAND = RANDSTICK
        if message.text:
            parts = message.text.split(maxsplit=1)
        elif message.caption:
            parts = message.caption.split(maxsplit=1)
        cmd_with_slash = parts[0]
        splitting = cmd_with_slash.lstrip("/").split("@")
        if len(splitting) > 1:
            afterdog = splitting[1]
        else:
            afterdog = "minercraftov_bot"
        if afterdog.lower() == "minercraftov_bot":
            cmd = splitting[0].lower()
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
            args = parts[1] if len(parts) > 1 else ""
            if cmd in chest["rich"][f"{chat_id}"]:
                await richagi(message, args, cmd)
            else:
                func = globals().get(cmd)
                if cmd == "richagi":
                    return
                if func:
                    await func(message, args)
            chest = openchest()

### ЗЕРКАЛО
    if chest["rich"][f"{chat_id}"]["lab"]:
        if message.text:
            original = message.text.replace(".", ",")
            await bot.send_message(chat_id=chat_id, text=original)
        if message.caption:
            original = message.caption.replace(".", ",")
        if message.photo:
            media = message.photo[-1].file_id
            await bot.send_photo(chat_id=chat_id, photo=media, caption=original or None)
        if message.animation:
            media = message.animation.file_id
            await bot.send_animation(chat_id=chat_id, animation=media, caption=original or None)
        if message.video:
            media = message.video.file_id
            await bot.send_video(chat_id=chat_id, video=media, caption=original or None)
        if message.sticker:
            media = message.sticker.file_id
            await bot.send_sticker(chat_id=chat_id, sticker=media)

    if mediaidcheck[user_id] and message.chat.type == "private":
        file_id = 0
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
        elif message.video:
            file_id = message.video.file_id
            unique_id = message.video.file_unique_id
        if file_id:
            await message.answer(
                f"ID: <code>{file_id}</code>\n"
                f"UNIQUE_ID: <code>{unique_id}</code>",
                parse_mode="HTML"
            )

### Реакция на текст
## Реакция на полный текст
    if message.text:
        if message.text.lower() == "кейн, купи пиво":
            await message.answer("Кейн, купи пиво")
        if message.text.lower() == "сколько пива":
            await message.answer("Пива мноооооооогоооо🍺🍺🍺🍺🍺")
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
        if message.chat.id == OT_ID and "все" in message.text.lower() and random.random() < 0.01:
            await message.reply_sticker(sticker=VSE_NIQ)
        if message.from_user.id == TIM_ID and any(word.lower().startswith(mat) for word in message.text.split() for mat in MATUUUK):
            chest["NUMB"] = chest["NUMB"] + 2
            await orluk(message, "")
        if "майнера крафтов" in message.text.lower():
            if message.from_user.id == TIM_ID:
                await message.reply("ты меня решил по полной разозлить >=( Моя сила ярости удвоена!")
                chest["NUMB"] = (chest["NUMB"]+1)*2
            else:
                await message.reply("не зли меня, бяка >=(")
## Реакция на стикеры
    if message.sticker:
        if message.sticker.file_unique_id in (VORO_UIQ, CRO_UIQ):
            await message.reply("Воро")
        if message.sticker.file_unique_id == VEI_UIQ:
            await message.reply_sticker(sticker=CHEZ_NIQ)
        if message.sticker.file_unique_id == ADALI_UIQ:
            await message.reply_sticker(sticker=MURA_NIQ)
    if message.animation:
        if message.from_user.id == TIM_ID:
            for key in chest["kazn"]:
                if chest["kazn"][key]["NOW"]:
                    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    if chest["kazn"][key]["TYPE"] == "use":
                        chest["kazn"][key]["NOW"] -= 1
            if chest["kazn"]["lv"]["NOW"]:
                chest["lv"]["NOW"] += 1
            if chest["kazn"]["sk"]["NOW"]:
                args = ""
                await rs(message, args)
            unique_id = message.animation.file_unique_id
            id = message.animation.file_id
            if f"{unique_id}" not in chest["GIFTIM"]:
                chest["GIFTIM"][f"{unique_id}"] = {}
                chest["GIFTIM"][f"{unique_id}"]["VALUE"] = 0
            chest["GIFTIM"][f"{unique_id}"]["GIF"] = id
            chest["GIFTIM"][f"{unique_id}"]["VALUE"] += 1
            chest["NUMB"] += chest["GIFTIM"][f"{unique_id}"]["VALUE"]
            print(f"ГИФКА ТИМА: {id}")
    closechest(chest)


















#### БУДИЛЬНИКИ
async def alarms():
### Сообщение админу о включении
    await bot.send_message(PEKO_ID, "доброе утро!")
### Сообщение чату о включении, если утро
#    if 7 <= MSKnow.hour < 13:
#        await bot.send_message(OT_ID, random.choice(GREETINGS))
### Сообщение о времени
    while True:
        now = datetime.now(MSK)
## Сообщение о 13:56
        if now.hour == 13 and now.minute == 56:
            await bot.send_photo(OT_ID, photo=VTRI_NIQ)
            await bot.send_photo(COVINOC_ID, photo=VTRI_NIQ)
            await asyncio.sleep(51)
## Сообщение о 19:52
        if now.hour == 19 and now.minute == 52:
            await bot.send_message(OT_ID, "📻📻📻")
            await asyncio.sleep(51)
        await asyncio.sleep(10)
async def pivtime():
    while True:
        await asyncio.sleep(60)
        if random.random() < 0.0005122:
            await bot.send_message(OT_ID, "Пивоминутка")
        chest = openchest()
        for key in chest["kazn"]:
            if chest["kazn"][key]["TYPE"] == "time":
                chest["kazn"][key]["NOW"] = max(0, chest["kazn"][key]["NOW"] - 1)
        closechest(chest)
async def timchill():
    while True:
        await asyncio.sleep(2400)
        chest = openchest()
        if chest["NUMB"] > 0:
            chest["NUMB"] -= 1
            closechest(chest)
async def send_sticker(cmd: str):
    packs = RANDSTICK.get(cmd)
    if not packs:
        print(f"а? чо єто? {cmd}")
        return
    pack = random.choice(packs)
    sp = await bot.get_sticker_set(pack)
    stickers = [s for s in sp.stickers if s.file_unique_id not in BAD_UIQ]
    if not stickers:
        print(f"У {pack} МАТЮЮЮЮЮЮЮЮЮЮЮЮК")
        return
    sticker = random.choice(stickers)
    await bot.send_sticker(OT_ID, sticker=sticker.file_id)
    print(f"Швирнула из {pack}")
async def console_sender():
    loop = asyncio.get_running_loop()
    print("Я пришла я тут я здесь я я")
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



        





















async deff sitecheck():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL_KEY, timeout=5) as resp:
                    logging.debug(f"ping NICE: {resp.status}")
        except Exception as e:
            logging.debug(f'ping RERORERO: {e}')
        await asyncio.sleep(600)

async def handle(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.debug("Webhook parse REROREROR:", e)
        return web.Response(text="Bad Request", status=400)
    return web.Response(text="OK", status=200)
async def on_startup(app):
    app["task1"] = asyncio.create_task(alarms())
    app["task2"] = asyncio.create_task(console_sender())
    app["task3"] = asyncio.create_task(pivtime())
    app["task4"] = asyncio.create_task(timchill())
    app["task5"] = asyncio.create_task(sitecheck())
async def on_cleanup(app):
    for name in ["task1", "task2", "task3", "task4", "task5"]:
        task = app.get(name)
        if task:
            task.cancel()
            try:
                await task
            except:
                pass

####запись и запуск бота
async def main():
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="OK", status=200))
    app.router.add_post("/webhook", handle)
    logging.basicConfig(level=logging.DEBUG)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    await bot.set_webhook(URL_KEY + "webhook")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await asyncio.Event().wait()
if __name__ == "__main__":
    asyncio.run(main())