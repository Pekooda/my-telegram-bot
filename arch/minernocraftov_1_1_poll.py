#### EVIL VERSION:
# 1.0 - BEGINNING OF DESTRUCTION
# 1.1 - Clear. No thing. Just.

import asyncio, os, logging, requests, aiohttp, random, re, json, html
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, Update, BufferedInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from collections import defaultdict, Counter
from aiohttp import web
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN = os.getenv("E_TOKEN_KEY")
PIXABAY_KEY = os.getenv("E_PIXABAY_KEY")
PEXELS_KEY = os.getenv("E_PEXELS_KEY")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
OT_ID = int(os.getenv("E_OT_ID"), 0)
COVINOC_ID = int(os.getenv("E_COVINOC_ID"), 0)
TIM_ID = int(os.getenv("E_TIM_ID"), 0)
MATUUUK = json.loads(os.getenv("E_MATUUUK", "[]"))
DEFAULT_QUERY = json.loads(os.getenv("E_DEFAULT_QUERY", '""'))
MNC_RAGE = json.loads(os.getenv("E_MNC_RAGE", '""'))
MNC_OVERRAGE = json.loads(os.getenv("E_MNC_OVERRAGE", '""'))

VSE_NIQ = os.getenv("E_VSE_NIQ")
URL = os.getenv("E_URL")



bot = Bot(token=TOKEN)
dp = Dispatcher()
TZ = timezone.utc
BOT_START = datetime.now(TZ)
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
bot_enabled = True
mediaidcheck = defaultdict(int)

chest = {
    "NUMB": 400,
    "kazn": {
        "st": {
            "NAME": "Banish of Time",
            "PRICE": 1,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "me destroy every GIF/Sticker from Tim in 1 minute",
            "TYPE": "time"
        },
        "lv": {
            "NAME": "Banish of Absorb",
            "PRICE": 3,
            "VALUE": 2,
            "NOW": 0,
            "INFO": "me absorb every GIF/Sticker from Tim, converting to additionaly minutes of banish in 2 minutes",
            "TYPE": "time"
        },
        "sk": {
            "NAME": "Banish of Convert",
            "PRICE": 2,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "me convert every GIF/Sticker from Tim to... nothing. Just a Voro Sticker in 1 minute",
            "TYPE": "time"
        },
        "ob": {
            "NAME": "Banish of Destroy",
            "PRICE": 3,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "me destroy next GIF/Sticker from Tim",
            "TYPE": "use"
        }
    },
    "GIFTIM": {},
    "rich": {}
}


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







async def start(message: types.Message, args: str):
    await message.answer("hiiii Me heeeereee... 😈😈")

async def evildata(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return
    global chest
    text = json.dumps(chest, indent=4, ensure_ascii=False)
    text = text.replace("true", "True").replace("false", "False")
    file = BufferedInputFile(
        text.encode("utf-8"),
        filename="evilchest.json"
    )
    await message.answer_document(file)

async def di(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Noo👿👿👿 You can use IT only in DM")
    user_id = message.from_user.id
    if mediaidcheck[user_id]:
        mediaidcheck[user_id] = False
        await message.answer("ID media sender is off. Enjoy it, for a while...")
    else:
        mediaidcheck[user_id] = True
        await message.answer("NOW YOU GET A ID media sender! YOUR MEDIA WILL BE DETECTED NOW! If you want to turn off it you can't... can't not use </di> again")


async def richagi(message: types.Message, args: str, cmd_name: str):
    if cmd_name == "cmt" and message.from_user.id == TIM_ID:
        return await message.reply("You have no power for it. You too weak... Eheheeee😈😈")
    texting = (message.text or "").split()
    if message.from_user.id == PEKO_ID and len(texting) > 2 and texting[2].lstrip("-").isdigit():
        chat_id = int(texting[2])
    else:
        chat_id = message.chat.id
    global chest
    cmd = chest["rich"][f"{chat_id}"][f"{cmd_name}"]
    if len(texting) < 2:
        return await message.reply(f"POWER OF {cmd_name}: {'🟢' if cmd else '🔴'} {cmd}\n\nIf you want to control the souls by yourself, type additionaly \"on\" or \"off\"")
    else:
        text = str(texting[1])
        if text == "on" and cmd:
            await message.reply(f"⚠️ Lever {cmd_name} is already on")
        elif text == "on" and not cmd:
            chest["rich"][f"{chat_id}"][f"{cmd_name}"] = True
            await message.reply(f"✅ Lever {cmd_name} turned on 🟢 True")
        elif text == "off" and not cmd:
            await message.reply(f"⚠️ Lever {cmd_name} is already off")
        elif text == "off" and cmd:
            chest["rich"][f"{chat_id}"][f"{cmd_name}"] = False
            await message.reply(f"✅ Lever {cmd_name} turned on 🔴 False")
        else:
            await message.reply(f"If you want to control the souls by yourself, type additionaly \"on\" or \"off\"")


###################
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

async def ping(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return
    set = False
    if args.startswith("!"):
        args = args.lstrip("!")
        set = True
    car = args.lstrip("-")
    if not car.isdigit():
        return await message.answer(f"I'm need a number...")
    global chest
    if set:
        chest["NUMB"] = int(args)
    else:
        chest["NUMB"] += int(args)
    await message.answer(f"Value of temperature in my cauldron now is {chest["NUMB"]}°C")

async def mercy(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return
    global chest
    for key in chest["kazn"]:
        chest["kazn"][key]["NOW"] = 0
    await message.answer(f"I'm absorbed all banishes from his soul, if you so...")

async def kotel(message: types.Message, args: str):
    if message.from_user.id == TIM_ID:
        return await message.answer("You can't control your own soul! 👿")
    chat_id = message.chat.id
    parts = (message.text or "").split()
    OVERRAGE = 0
    global chest
    for key in chest["kazn"].values():
        OVERRAGE += key.get("NOW", 0)
    RAGE = html.escape(rage_meter(chest["NUMB"] + OVERRAGE, MNC_RAGE))
    POVERRAGE = html.escape(rage_meter(OVERRAGE, MNC_OVERRAGE))
    if len(parts) < 2:
        nanameme = []
        for subname, key in chest["kazn"].items():
            template = f"""
{"🟢" if key.get("NOW", 0) else "⚪️"} {key.get("NAME", "NO NAME")} - {key.get("INFO", "NO DESC")}
{"Number of uses now" if key.get("TYPE", 0) == "use" else "Time of use now"}: {key.get("NOW", "???")} {"mins" if key.get("TYPE", 0) == "time" else ""}
Value of temperature in my cauldron to use the banish: {key.get("PRICE", "???")}°C
To activate it, type <code>/kotel {subname}</code>"""
            nanameme.append(template)
        info = "<blockquote expandable>" + "".join(nanameme).strip() + "</blockquote>"
        return await message.answer(f"""
The value of temperature in my cauldron: {chest["NUMB"]}°C
<b>{RAGE}{POVERRAGE}</b>
You can exchange the temperature in my cauldron to:
{info}
If you want a bigger value type a number after type of banish
""", parse_mode="HTML")
    id = str(parts[1])
    if not parts[1] in chest["kazn"].keys():
        return await message.answer(f"I don't know that type of banish 👿")
    COUNT = nozerolast(parts, 2)
    if not COUNT:
        return await message.answer(f"Nonono, you can use only digital values of number")
    n = chest["kazn"][id]["NAME"]
    p = chest["kazn"][id]["PRICE"] * COUNT
    v = chest["kazn"][id]["VALUE"] * COUNT
    if chest["NUMB"] < p:
        return await bot.send_message(chat_id, f"""
The temperature in my cauldron is too low for it!
I'm need a {p}°C in my cauldron at least to use it.
The temperature in my cauldron for now: {chest["NUMB"]}°C
""")
    chest["NUMB"] -= p
    chest["kazn"][id]["NOW"] += v
    await bot.send_message(chat_id, f"""
{n} is on!
{"Number of uses now" if chest["kazn"][id]["TYPE"] == "use" else "Time of use now"}: {chest["kazn"][id]["NOW"]} {"mins" if chest["kazn"][id]["TYPE"] == "time" else ""}
The temperature in my cauldron for now: {chest["NUMB"]}°C
""")

#{"Number of uses now" if chest["NUMB"][id]["TYPE"] == "use" else "Time of use now"}: {chest["kazn"][id]["NOW"]} {"mins" if chest["NUMB"][id]["TYPE"] == "time" else ""}

def MATUK_CHECK(text):
    for w in MATUUUK:
        pattern = rf"^{re.escape(w)}\w*"
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False

async def orluk(message: types.Message, args: str):
    query = "орел"
    tes = random.choice([erv, erv1, erp, erp1])
    eagle = await tes(message, query)
    if tes in (erp, erp1):
        await message.answer_photo(eagle)
    else:
        await message.answer_animation(eagle)

def queryfilter(message, query, com):
    R = message.text.startswith(f"/{com}")
    if message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT_QUERY)
    if bool(re.search(r'[\u0400-\u04FF]', query)):
        query = "злой " + query
    else:
        query = "evil " + query
    return R, query


async def erp(message: types.Message, query: str):
    erP, query = queryfilter(message, query, "erp")
    params = {"key": PIXABAY_KEY, "q": query, "image_type": "photo", "safesearch": "true", "per_page": 200}
    try:
        resp = requests.get("https://pixabay.com/api/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        if erP:
            return await message.reply(f"ERRORERROR: {e}")
        else:
            return "no"
    if not hits:
        if erP:
            return await message.reply("There is no free souls for it. How sad.")
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
    if erP:
        await message.answer_photo(img_url)
    else:
        return img_url


async def erv(message: types.Message, query: str):
    erV, query = queryfilter(message, query, "erv")
    params = {"key": PIXABAY_KEY, "q": query, "video_type": "all", "per_page": 199}
    try:
        resp = requests.get("https://pixabay.com/api/videos/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        if erV:
            return await message.reply(f"ERRORERROR: {e}")
        else:
            return "no"
    if not hits:
        if erV:
            return await message.reply("There is no free souls for it. How sad.")
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
            if erV:
                return await message.answer_animation(video_url)
            else:
                return video_url



async def erp1(message: types.Message, query: str):
    erP1, query = queryfilter(message, query, "erp1")
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/v1/search", params=params, headers=key, timeout=5)
        data = resp.json()
        photos = data.get("photos", [])
    except Exception as e:
        if erP1:
            return await message.reply("ERRORERROR: {e}")
        else:
            return "no"
    if not photos:
        if erP1:
            return await message.reply(f"There is no free souls for it. How sad.")
        else:
            return "no"
    choice = random.choice(photos)
    img_url = choice["src"]["large"]
    if erP1:
        await message.answer_photo(img_url)
    else:
        return img_url


async def erv1(message: types.Message, query: str):
    erV1, query = queryfilter(message, query, "erv1")
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": 75, "locale": "ru-RU"}
    try:
        resp = requests.get("https://api.pexels.com/videos/search", params=params, headers=key, timeout=5)
        data = resp.json()
        videos = data.get("videos", [])
    except Exception as e:
        if erV1:
            return await message.reply(f"ERRORERROR: {e}")
        else:
            return "no"
    if not videos:
        if erV1:
            return await message.reply("There is no free souls for it. How sad.")
        else:
            return "no"
    choice = random.choice(videos)
    url = choice["video_files"][0]["link"]
    video_url = url.replace("http://", "https://")
    if erV1:
        await message.answer_animation(video_url)
    else:
        return video_url

async def pokapoka(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("No. You can't. And how did you know, huh? 👿")
    if not args:
        return await message.reply("From where i'm need to leave?")
    if args.startswith("-100"):
        leaveid = int(args)
        try:
            await bot.leave_chat(leaveid)
            return await message.reply("Yay, I leave this souls alone 😈😈😈")
        except Exception as e:
            return await message.reply("I'm not in this place even")
    await message.reply("This is even not a chat 👿")

async def text(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("No. You can't. And how did you know, huh? 👿")
    texting = (message.text or "").split()
    if len(texting) < 3:
        return await message.reply("I'm need A TEXT")
    m = str(texting[1])
    val = {
        "!1": OT_ID,
        "!2": COVINOC_ID,
        "!40": PEKO_ID
    }
    mes_id = str(val.get(m, m))
    if not mes_id.lstrip("-").isdigit():
        return await message.reply(f"I'M NEED ID: /text <ID> <text>\n\nOr shortcuts")
    texting = (message.text or "").split(maxsplit=2)
    d = str(texting[2])
    try:
        NAME = await bot.get_chat(mes_id)
        chat = NAME.title or NAME.full_name
        await bot.send_message(mes_id, d)
        await message.reply(f"I'm wrote in [{chat}]: {d}")
    except Exception as e:
        await message.reply(f"I'm even not in this place 👿")








@dp.message()
async def vse(message: Message):
    if not message.date < BOT_START and message.text and message.text.lower().startswith("майнер некрафтов, "):
        global bot_enabled
        if message.text.lower() == "майнер некрафтов, спать":
            if not bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("No, I'm not gonna to sleep 👿")
            bot_enabled = False
            return await message.reply("Ok. Now I can rest...")
        elif message.text.lower() == "майнер некрафтов, проснуться":
            if bot_enabled:
                return
            if message.from_user.id != PEKO_ID:
                return await message.reply("No, I'm not gonna wake up 👿")
            bot_enabled = True
            return await message.reply("Evil morning, my little souls, are you ready? 😈😈")
    if not bot_enabled:
        return
    global chest
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.date < BOT_START:
        return
    if f"{chat_id}" not in chest["rich"]:
        chest["rich"][f"{chat_id}"] = {
            "cmt": False
        }
    if message.from_user.id == TIM_ID and chest["rich"][f"{chat_id}"]["cmt"]:
        try:
            return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        except Exception as e:
            pass
    if (message.text and message.text.startswith("/")) or (message.caption and message.caption.startswith("/")):
        if message.text:
            parts = message.text.split(maxsplit=1)
        elif message.caption:
            parts = message.caption.split(maxsplit=1)
        cmd_with_slash = parts[0]
        splitting = cmd_with_slash.lstrip("/").split("@")
        if len(splitting) > 1:
            afterdog = splitting[1]
        else:
            afterdog = "minernocraftov_bot"
        if afterdog.lower() == "minernocraftov_bot":
            cmd = splitting[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            if cmd in chest["rich"][f"{chat_id}"]:
                await richagi(message, args, cmd)
            else:
                func = globals().get(cmd)
                if cmd == "richagi":
                    return
                if func:
                    await func(message, args)
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
                f"DI: <code>{file_id}</code>\n"
                f"UGLY_DI: <code>{unique_id}</code>",
                parse_mode="HTML"
            )
    if message.text:
        if message.text.lower() == "воро":
            await message.answer("Воро")
        if message.chat.id == OT_ID and "все" in message.text.lower() and random.random() < 0.01:
            await message.reply_sticker(sticker=VSE_NIQ)
        if message.from_user.id == TIM_ID and any(word.lower().startswith(mat) for word in message.text.split() for mat in MATUUUK):
            chest["NUMB"] = chest["NUMB"] + 2
            await orluk(message, "")
    if message.animation or message.sticker:
        if message.from_user.id == TIM_ID:
            for key in chest["kazn"]:
                if chest["kazn"][key]["NOW"]:
                    try:
                        await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    except Exception as e:
                        pass
                    if chest["kazn"][key]["TYPE"] == "use":
                        chest["kazn"][key]["NOW"] -= 1
            if chest["kazn"]["lv"]["NOW"]:
                chest["lv"]["NOW"] += 1
            if chest["kazn"]["sk"]["NOW"]:
                await message.answer_sticker(sticker=VORO_NIQ)
            if message.animation:
                unique_id = message.animation.file_unique_id
                id = message.animation.file_id
            if message.sticker:
                unique_id = message.sticker.file_unique_id
                id = message.sticker.file_id
            if f"{unique_id}" not in chest["GIFTIM"]:
                chest["GIFTIM"][f"{unique_id}"] = {}
                chest["GIFTIM"][f"{unique_id}"]["VALUE"] = 0
            chest["GIFTIM"][f"{unique_id}"]["GIF"] = id
            chest["GIFTIM"][f"{unique_id}"]["VALUE"] += 1
            chest["NUMB"] += chest["GIFTIM"][f"{unique_id}"]["VALUE"]

async def alarms():
    await bot.send_message(PEKO_ID, "Evil evening!")
    while True:
        for i in range(60):
            await asyncio.sleep(60)
            global chest
            for key in chest["kazn"]:
                if chest["kazn"][key]["TYPE"] == "time":
                    chest["kazn"][key]["NOW"] = max(0, chest["kazn"][key]["NOW"] - 1)
        if chest["NUMB"] > 0:
            chest["NUMB"] -= 1


####запись и запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=False)
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=False),
        alarms(),
        pivtime(),
        timchill()
    )
    for t in pending:
        t.cancel()
    try:
        await bot.session.close()
    except Exception:
        pass
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"я спать пошла, спокойной ночи\n")