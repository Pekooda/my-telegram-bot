#### EVIL VERSION:
# 1.0 - BEGINNING OF DESTRUCTION

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
HURM_ID = int(os.getenv("E_HURM_ID"), 0)
TIM_ID = int(os.getenv("E_TIM_ID"), 0)
EVILNINGS = json.loads(os.getenv("E_EVILNINGS", "[]"))
MATUUUK = json.loads(os.getenv("E_MATUUUK", "[]"))
DEFAULT_QUERY = json.loads(os.getenv("E_DEFAULT_QUERY", '""'))
MNC_RAGE = json.loads(os.getenv("E_MNC_RAGE", '""'))
MNC_OVERRAGE = json.loads(os.getenv("E_MNC_OVERRAGE", '""'))

MURA_NIQ = os.getenv("E_MURA_NIQ")
CHEZ_NIQ = os.getenv("E_CHEZ_NIQ")
MAX_NIQ = os.getenv("E_MAX_NIQ")
LEAFY_NIQ = os.getenv("E_LEAFY_NIQ")
VSE_NIQ = os.getenv("E_VSE_NIQ")
VTRI_NIQ = os.getenv("E_VTRI_NIQ")
VORO_UIQ = os.getenv("E_VORO_UIQ")
VORO_NIQ = os.getenv("E_VORO_NIQ")
CRO_UIQ = os.getenv("E_CRO_UIQ")
VEI_UIQ = os.getenv("E_VEI_UIQ")
ADALI_UIQ = os.getenv("E_ADALI_UIQ")
EVEI_UIQ = os.getenv("E_VEI_UIQ")
EADALI_UIQ = os.getenv("E_ADALI_UIQ")
URL = os.getenv("E_URL")
SAD_UIQ = json.loads(os.getenv("E_SAD_UIQ", "[]"))



bot = Bot(token=TOKEN)
dp = Dispatcher()
TZ = timezone.utc
BOT_START = datetime.now(TZ)
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
bot_enabled = True
mediaidcheck = defaultdict(int)

chest = {
    "NUMB": 270,
    "kazn": {
        "st": {
            "NAME": "Banish of Time",
            "PRICE": 3,
            "VALUE": 5,
            "NOW": 0,
            "INFO": "in 5 minutes I'll destroy every GIF/Sticker from Tim",
            "TYPE": "time"
        },
        "lv": {
            "NAME": "Banish of Absorb",
            "PRICE": 3,
            "VALUE": 3,
            "NOW": 0,
            "INFO": "in 3 minutes I'll absorb every GIF/Sticker from Tim, converting to additionaly minutes of banish",
            "TYPE": "time"
        },
        "sk": {
            "NAME": "Banish of Convert",
            "PRICE": 3,
            "VALUE": 4,
            "NOW": 0,
            "INFO": "in 4 minutes I'll convert every GIF/Sticker from Tim to... nothing. Just a Voro Sticker",
            "TYPE": "time"
        },
        "ob": {
            "NAME": "Banish of Destroy",
            "PRICE": 3,
            "VALUE": 5,
            "NOW": 0,
            "INFO": "i'll destroy next 5 GIF/Stickers from Tim",
            "TYPE": "use"
        }
    },
    "GIFTIM": {
        "AgADpwUAAvOSdVE": {
            "VALUE": 1
        },
        "AgAD_wIAAkAaTVM": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIYGGmzQQHPAgWqKJtA5w_SrKSSRz3sAAL_AgACQBpNU76nd4Ed73pIOgQ"
        },
        "AgADDQMAAiRStVM": {
            "VALUE": 2
        },
        "AgAD6gUAAjFZNVA": {
            "VALUE": 1
        },
        "AgADCGwAAqFHEEs": {
            "VALUE": 1
        },
        "AgADWQYAAvJQ_FE": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIbg2m0DHXKEBQ6Ff0tnS42WX4FnAuSAAJZBgAC8lD8UbImUZBCEg3xOgQ"
        },
        "AgAD6IoAAl6kKUk": {
            "VALUE": 8,
            "GIF": "CgACAgIAAyEFAATmi0vRAAIgUWm0WjGjnsVLeBo2kGv2s2_QueChAALoigACXqQpSebzr8UAAUaDDToE"
        },
        "AgADtgIAAnXUDFM": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIjb2m1kDezOnnXJsBWh1NPt0KGfNTqAAK2AgACddQMU26TMBFnr3kCOgQ"
        },
        "AgADV40AAl6f2Uk": {
            "VALUE": 1
        },
        "AgADHgMAAqCfDFM": {
            "VALUE": 15,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIg4Gm0frazCeSCijOgORnW_lFaWoiJAAIeAwACoJ8MUxb7XMFAF3iAOgQ"
        },
        "AgADOwYAAiIHxVM": {
            "VALUE": 1
        },
        "AgAD9gkAAsrYVVE": {
            "VALUE": 18,
            "WHAT": "Гифка с плюшевым Яроном",
            "GIF": "CgACAgQAAyEFAATCPNLXAAECtZ1pttJoQO5BSeeM4HfmcNo9tvRlogAC9gkAAsrYVVE-Je4QnlNhwjoE"
        },
        "AgADQZQAAibRyUo": {
            "VALUE": 2,
            "GIF": "CgACAgIAAyEFAATCPNLXAAECl6VpsrHne3ye3pWe_th-FD6CmQkfygACQZQAAibRyUpuPPwnjHP1EToE"
        },
        "AgAD6wMAAmOntVE": {
            "VALUE": 1
        },
        "AgAD8AIAAkkNDVM": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIwm2m4WaTYw-h1HSuLf29-oBlz9aOKAALwAgACSQ0NU4VbzP5zv4fDOgQ"
        },
        "AgADMgYAAhJ6DVI": {
            "VALUE": 1
        },
        "AgAD_QIAAr6wBFM": {
            "VALUE": 1
        },
        "AgADnwIAAl3UDFM": {
            "VALUE": 2,
            "GIF": "CgACAgQAAyEFAATmi0vRAAI1Imm630-sqAjkypgdiihv-f5i4Fb8AAKfAgACXdQMU2y4Z-ts_Q8WOgQ"
        },
        "AgADQwgAAkPxLVI": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIxjWm5Zc4NyZUe-PV9PuJQmn503PJWAAJDCAACQ_EtUpWjDEWPVVvuOgQ"
        },
        "AgADnAcAAkVUnFM": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAI4Umm8M34QPC-bbd10kQ3r6rxJLP4dAAKcBwACRVScU3NkOB8ZRkRtOgQ"
        },
        "AgADpQYAArJg5VI": {
            "VALUE": 3,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIUSGmyzpw3j6AWmm3OLd15-rFbl2WYAAKlBgACsmDlUiz40Yrf4ujVOgQ"
        },
        "AgADUggAAhTNLVI": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIxk2m5ZiyvTX8g2CWZI7Xuw6BeTRBhAAJSCAACFM0tUuwhw0IvN-XzOgQ"
        },
        "AgADaAMAAtjXhFA": {
            "VALUE": 3,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJDUWm_1qHfthVMF7HqIWlt0HEpu6yWAAJoAwAC2NeEUJjJF6rWpl3oOgQ"
        },
        "AgAD_WkAAqS9IEg": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATmi0vRAAIvrmm3_lHcYcklRkcQtVnpMmCmeTllAAL9aQACpL0gSCjpxve-v0StOgQ"
        },
        "AgADiQoAAjDZEUk": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATCPNLXAAECl3xpsq82u8OvEecvJmJuBV2v_olm-QACiQoAAjDZEUnXlSm9BUvNbzoE"
        },
        "AgADwQoAAnC2CUk": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATCPNLXAAECmLBpsr0crKDcHaWtvFvJ2ruYl9YESQACwQoAAnC2CUkewImgAv8_bzoE"
        },
        "AgAD0QcAAjoTEEk": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATCPNLXAAECl5RpsrC2Sw6swpsTjP5pCUBwFhAMUQAC0QcAAjoTEEnLdGDcC0VEfzoE"
        },
        "AgADcZ0AAjFYQUk": {
            "VALUE": 1,
            "GIF": "CAACAgIAAxUAAWmz-bQov1Vd186iI4sQK5InRJdTAAJxnQACMVhBSUtMlJ5AnUY0OgQ"
        },
        "AgADUAQAAkpFBVA": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAITSmmymNg7XOJW4HbAc0KhgRvsQiVdAAJQBAACSkUFUL_DwHdMVuAhOgQ"
        }
    },
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







async def destroy(message: types.Message, args: str):
    rand = random.randint(-1000, 0)
    await message.answer(f"DO YOU WANNA DESTROY? I'M WANNA IT! TIME OF BEGINNING OF DESTROYING: {MSKnow}. POWER: {rand}")

async def evildata(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.reply("Nooo, you can't get that secret files! 👿👿👿")
    global chest
    text = json.dumps(chest, indent=2, ensure_ascii=False)
    file = BufferedInputFile(
        text.encode("utf-8"),
        filename="evilchest.json"
    )
    await message.answer_document(file)

async def banmin(message: types.Message, args: str):
    if random.random() < 0.0003619:
        await message.answer("YES! I'M GRANTING YOU A TITLE OF BANMIN!")

async def ee(message: types.Message, args: str):
    await message.reply(random.choice(EVILNINGS) + " 😈")

async def di(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.reply(f"Noo👿👿👿 You can use IT only in DM")
    user_id = message.from_user.id
    if mediaidcheck[user_id]:
        mediaidcheck[user_id] = False
        await message.answer("ID media sender is off. Enjoy it, for a while...")
    else:
        mediaidcheck[user_id] = True
        await message.answer("NOW YOU GET A ID media sender! YOUR MEDIA WILL BE DETECTED NOW! If you want to turn off it you can't... can't not use /di again")

async def dislike(message: types.Message, args: str):
    quer = message.text.split(maxsplit=1)
    query = quer[1].strip() if len(quer) > 1 else "👎"
    try:
        success = await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=(message.reply_to_message.message_id if message.reply_to_message is not None else message.message_id),
            reaction=[{"type": "emoji", "emoji": query}]
        )
    except Exception as e:
        return await message.reply("I don't know that thing 👿")

async def richagi(message: types.Message, args: str, cmd_name: str):
    if cmd_name == ("cmh" or "cry") and message.from_user.id == HURM_ID:
        return await message.reply("You have no power for it. You too weak...")
    if cmd_name == "tdt" and message.from_user.id == TIM_ID:
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
            await message.reply(f"✅ Рычаг {cmd_name} turned on 🔴 False")
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
        return await message.answer(f"You can't control his soul! 👿")
    set = False
    if args.startswith("!"):
        args = args.lstrip("!")
        set = True
    if not args.isdigit():
        return await message.answer(f"I'm need a number...")
    global chest
    if set:
        chest["NUMB"] = int(args)
    else:
        chest["NUMB"] += int(args)
    await message.answer(f"Value of temperature in my cauldron now is {chest["NUMB"]}°C")

async def mercy(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return await message.answer("You can't control his soul! 👿")
    global chest
    for key in chest["kazn"]:
        chest["kazn"][key]["NOW"] = 0
    await message.answer(f"I'm absorbed all banishes from his soul, if you so...")



async def cauldron(message: types.Message, args: str):
    if message.from_user.id == TIM_ID:
        return await message.answer("You can't control your own soul! 👿")
    if message.chat.id != OT_ID and message.from_user.id != PEKO_ID:
        return await message.answer(f"No no no, I can't control his soul out of cauldon. Only near the cauldron.")
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
To activate it, type <code>/cauldron {subname}</code>"""
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
    if not message.date < BOT_START and message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["cry"] and ((message.text and message.text in ("😭", "🥺")) or (message.sticker and message.sticker.file_unique_id in SAD_UIQ)):
        return await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if message.chat.id == OT_ID and random.random() < 0.00025: 
        if random.random() < 0.01:
            await message.reply("IT MESSAGE MAKES ME THE HAPPIEST DEMON IN HELL!!!! 😈😈😈, 1 TO 400000")
        elif random.random() < 0.1: 
            await message.reply("IT MESSAGE MAKES ME SOOOO HAPPY, THAT YOU CANT 😈😈, 1 TO 40000")
        else:
            await message.reply("IT MESSAGE MAKES ME HAPPY 😈")
    if message.date < BOT_START:
        return
    if message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["cmh"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.from_user.id == TIM_ID and chest["rich"][f"{chat_id}"]["tdt"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if f"{chat_id}" not in chest["rich"]:
        chest["rich"][f"{chat_id}"] = {
            "zer": False,
            "cmh": False,
            "tdt": False,
            "cry": True
        }
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
    if chest["rich"][f"{chat_id}"]["zer"]:
        if message.text:
            original = message.text.replace(",", ".")
            await bot.send_message(chat_id=chat_id, text=original)
        if message.caption:
            original = message.caption.replace(",", ".")
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
                f"DI: <code>{file_id}</code>\n"
                f"UGLY_DI: <code>{unique_id}</code>",
                parse_mode="HTML"
            )
    if message.text:
        if message.text.lower() == "кейн, купи пиво":
            await message.answer("Kane, sell a beer")
        if message.text.lower() == "сколько пива":
            await message.answer("BEER IS NOT ENOUGH, I'M WARN YOU, BEER IS NOT ENOUGH!!!🍺🍺🍺🍺🍺")
        if message.text.lower() == "я вернулся":
            await message.answer_sticker(sticker=MAX_NIQ)
        if message.text.lower() == "кобо":
            await message.answer("Actually a robotic dumb voice")
        if message.text.lower() in ("муравей", "insect"):
            await message.reply_sticker(sticker=CHEZ_NIQ)
        if message.text.lower() in ("че задали", "wha cancelled"):
            await message.reply_sticker(sticker=MURA_NIQ)
        if message.text.lower() == "воро":
            await message.answer("Cro")
        if message.text.lower() == "2763":
            await message.reply_sticker(sticker=LEAFY_NIQ)
## Реакция на текст в сообщении
        if message.chat.id == OT_ID and "все" in message.text.lower() and random.random() < 0.01:
            await message.reply_sticker(sticker=VSE_NIQ)
        if message.from_user.id == TIM_ID and any(word.lower().startswith(mat) for word in message.text.split() for mat in MATUUUK):
            chest["NUMB"] = chest["NUMB"] + 2
            await orluk(message, "")
    if message.sticker:
        if message.sticker.file_unique_id in (VORO_UIQ, CRO_UIQ):
            await message.reply("cro")
        if message.sticker.file_unique_id in (ADALI_UIQ, EADALI_UIQ):
            await message.reply_sticker(sticker=CHEZ_NIQ)
        if message.sticker.file_unique_id in (VEI_UIQ, EVEI_UIQ):
            await message.reply_sticker(sticker=MURA_NIQ)
    if message.animation or message.sticker:
        if message.from_user.id == TIM_ID:
            for key in chest["kazn"]:
                if chest["kazn"][key]["NOW"]:
                    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    if chest["kazn"][key]["TYPE"] == "use":
                        chest["kazn"][key]["NOW"] -= 1
            if chest["kazn"]["lv"]["NOW"]:
                chest["lv"]["NOW"] += 1
            if chest["kazn"]["sk"]["NOW"]:
                await message.reply_sticker(sticker=VORO_NIQ)
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
            print(f"GIF OR STICKER of TIM: {id}")


















async def alarms():
    await bot.send_message(PEKO_ID, "Evil evening!")
    while True:
        now = datetime.now(MSK)
        if now.hour == 13 and now.minute == 56:
            try:
                await bot.send_photo(OT_ID, photo=VTRI_NIQ)
                await bot.send_photo(COVINOC_ID, photo=VTRI_NIQ)
                await asyncio.sleep(51)
            except Exception as e:
                pass
        if now.hour == 19 and now.minute == 52:
            try:
                await bot.send_message(OT_ID, "📺📺📺")
                await asyncio.sleep(51)
            except Exception as e:
                pass
        await asyncio.sleep(10)
async def pivtime():
    while True:
        await asyncio.sleep(60)
        if random.random() < 0.000025:
            await bot.send_message(OT_ID, "Juiceminute")
        global chest
        for key in chest["kazn"]:
            if chest["kazn"][key]["TYPE"] == "time":
                chest["kazn"][key]["NOW"] = max(0, chest["kazn"][key]["NOW"] - 1)
async def timchill():
    while True:
        await asyncio.sleep(2400)
        global chest
        if chest["NUMB"] > 0:
            chest["NUMB"] -= 1
async def pingser():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=5) as resp:
                    logging.debug(f"ping NICE: {resp.status}")
        except Exception as e:
            logging.debug(f'ping RERORERO: {e}')
        await asyncio.sleep(300)



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
    app["task2"] = asyncio.create_task(pivtime())
    app["task3"] = asyncio.create_task(timchill())
    app["task4"] = asyncio.create_task(pingser())
async def on_cleanup(app):
    for name in ["task1", "task2", "task3", "task4"]:
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
    await bot.set_webhook(URL + "webhook")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())