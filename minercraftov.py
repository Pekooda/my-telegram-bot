import asyncio, logging, random, re, requests, sys, inspect, html, os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.enums import ParseMode
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone, time

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
BOT_START = datetime.now(timezone.utc)
bot_enabled = True
ADMIN_ID = 5513644023
JUNKR = 5134703218
CHAT_ID = -1002385589532
WRITE = -1002385589532
HURMO = 7313905505
lab = False
ODA = False
TZ = timezone.utc
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
TEXT = "я ничо не писала"
TARGET = datetime(2026, 1, 9, 0, 0, tzinfo=MSK)
TARGET1 = datetime(2026, 1, 10, 0, 0, tzinfo=MSK)
LWK = datetime(MSKnow.year, MSKnow.month, MSKnow.day, 7, 42, 10, tzinfo=MSK)

BAD = {"AgADoAcAApXm4UY", "AgADQxQAAuzDuUg", "AgADXRYAAg7iQUg", "AgADKxgAAogoSUg", "AgAD6REAAvONSEg", "AgADxhcAAimBQUg", "AgADbBYAAnyieEs", "AgADcRcAAvixeUs", "AgADYBMAAphCeUs", "AgADnxMAArCJeUs", "AgADHhMAAgxeeUs", "AgADLhYAAlmNeEs", "AgADkhYAAnIfeUs", "AgADJwAD-5IlBg", "AgAD6DwAApI1wEg", "AgAD0DsAAvFJwEg", "AgADB0EAAmdQwEg", "AgADBkQAAgdiwEg", "AgADhDwAAjKPyEg", "AgADRjoAAsrnwEg", "AgADhD0AAqWtwEg", "AgADVToAAiF8wUg", "AgADkTgAAmqcwEg", "AgADRzkAAoQ1wUg", "AgADHT4AAg-ewEg", "AgADXj0AAmtJwUg", "AgADdEEAAr52wUg", "AgADfkkAAiJgwEo", "AgAD20QAAnjkwEo", "AgADwTcAAjE7IEk", "AgADkxQAAkFlsEs", "AgADBhYAAkZLqEs", "AgADFBYAAlmFwEo", "AgAD-SMAAr0g2Eg", "AgAD5x4AAkA22Eg", "AgADiB4AAmdISEg", "AgAD0iMAAsNkSEg", "AgADhR0AAs5DSEg", "AgAD2yIAAneRSUg", "AgAD3R4AAstPSUg", "AgADYCUAAtVgwUs", "AgADCRcAAqmfyUs", "AgADSB0AAoUvwEs", "AgADcBsAAu_wwEs", "AgADKx4AAoFjWEs", "AgADohwAA1NYSw", "AgADohkAAqEsUUs", "AgAD0h8AAvesOEs", "AgADrRsAAi_n-Eo", "AgADgBkAAiZaeEo", "AgADLB0AAnOkwEk", "AgADQxoAAj5UyUk", "AgADZRYAArUvAAFK", "AgADsV0AAstqyUs", "AgADFlwAAqp5-Eg", "AgADimkAAoSdIEg", "AgADMWEAApisSUo", "AgAD9mwAAvUYYEo", "AgADOmQAAnp98Eg", "AgADmGwAAhy6IUk", "AgADE1oAAql8OUs", "AgAD_G8AAtNrmUo", "AgADfwEAAokqwFU", "AgADH00AAlXhwUk", "AgADT1QAAtMgyUk", "AgADpmUAAgUf6Us", "AgAD9WAAAneYwUs", "AgADRlwAAhhAyUs", "AgADngADvo8yGA", "AgADhgADvo8yGA", "AgADywADvo8yGA", "AgADfwADvo8yGA", "AgADhAADvo8yGA", "AgADsgADvo8yGA", "AgADrXkAAlO3kUg", "AgADvSgAAlE9wUo", "AgADVisAArYSwEo", "AgADOCoAAqSOwEo", "AgADPyIAAtxtyEo", "AgADwSEAAoo5yUo", "AgADbSQAAqYiwUo", "AgADkCwAAj34wUo", "AgADA1sAAs__0Es", "AgADFB4AApl6mEs", "AgAD6SAAAnX7oUs", "AgADEh4AAtYkoUs", "AgADEiIAArb5oEs", "AgADSiEAAnzeoUs", "AgADJSIAAm91mEs", "AgADuR4AAhhCmEs", "AgADpBsAAqm8oEs", "AgADHCAAAq8NmEs", "AgAD9x8AAuwRmEs", "AgADFiIAAvfsmEs", "AgAD9yAAAkDpmUs", "AgAD2CIAAor5oUs", "AgADcR8AApb6mUs", "AgADdiEAAuRfoEs", "AgADaCMAAhQLmUs", "AgADpR4AAqujmUs", "AgADqyEAAjdymEs", "AgADeR8AApACmEs", "AgADJh4AAgvnmEs", "AgADvyIAAtglmEs", "AgADwSAAAr-qoUs", "AgADCSIAAvKpmUs", "AgADUiEAAmyZoEs", "AgADsCoAAiyImUs", "AgADmCIAAq83mEs", "AgADRiUAAoHAmEs", "AgADTRsAAnFfmEs", "AgADlCAAAoQrmUs", "AgADAR8AAnOhoUs", "AgADqx8AAgrjmEs", "AgADkyAAAtgDmUs", "AgADuiEAAqFMmEs", "AgADvxwAAsdqoEs", "AgADzCAAAkO_oUs", "AgADuyUAAjn0oEs", "AgADJSIAAho_mUs", "AgADUh8AAniwoEs", "AgADESAAAmkHmEs", "AgADGi0AAoi5oUs", "AgADJCIAAiQvoUs", "AgADWCIAAqzRoEs", "AgAD-BoAArbdmEs", "AgADcCAAAqbBmUs", "AgADbB4AAqEvoEs", "AgADdCIAAmEMoUs", "AgADjiIAAgP6oUs", "AgADESIAAu-FoUs", "AgADxR8AAkobmUs", "AgADLB8AAuR3oEs", "AgADvh8AAhKooEs", "AgADCR4AAgejqUs", "AgADgh8AAjjTmUs", "AgADSx4AArP-oEs", "AgADBD8AAtO9GEg", "AgAD-i0AAmtqwUo", "AgADvBgAAl6ISUk", "AgADdmwAAkyASUo", "AgADpWIAAhMEyEs", "AgADmTQAAiBHwEk", "AgAD0iwAAgQu2Uk", "AgADDysAAnbrAUg", "AgAD0WcAAtAtSEo", "AgADomUAAn2pGUs", "AgADq3QAAtu9GUs", "AgADw3AAAsr0OEs", "AgADpXEAAvsimUs", "AgADMmkAAgWZOUo", "AgADuWIAAggEOUo", "AgADdmwAAkyASUo", "AgADgzoAAtOJAUg", "AgADSzkAAv3tAUg", "AgAD0igAApFL4Eg", "AgADCSkAAs_O4Ug", "AgAD9SkAAghD4Ug", "AgADciUAApi44Eg", "AgADRD0AArTgaUo", "AgADMUAAAxloSg", "AgADcUIAAgtnyUs", "AgADL3QAApQ7qUs", "AgADcnkAAtsSsUs", "AgAD8BoAApVeoUk", "AgAD3hsAAqLkmEk", "AgAD1nUAAuA3eEk", "AgADRUkAAoCZ6Uk", "AgADJUYAAjIF6Ek", "AgADvkEAAibb8Uk", "AgADtkIAApAQMUo", "AgADVUEAAuZfMUo", "AgADzUEAAntHMUo", "AgADBwUAAggtGUQ", "AgADqgYAAtN0OEc", "AgADpj0AAi--QUo", "AgADmBIAAmc1iEk", "AgADV1QAAi7fGEg", "AgAD0B4AApLNeEk", "AgADMRoAAusAAYFJ", "AgAD1RwAAhsceUk", "AgADghkAAgineUk", "AgAD9CkAAlO2iEs", "AgADmBsAAo5YiUs", "AgADOBsAAmcJ2Uo", "AgADZhcAAjRh4Uo"}
MAX_TRIES = 10

def format_menu_text(commands_map: dict) -> str:
    lines = [""]
    for cmd in commands_map.keys():
        lines.append(f"/{cmd}\n")
    return "".join(lines)


#пиксебей
PIXABAY_KEY   = "50465322-eaafc6cab26134551397d7139"
PEXELS_KEY = "awStroXjhtKGUbg63QfNc3AYJVwzpSIj1HcvO7BYc6wRSISfdgC7CsIr"
DEFAULT = [""]

#реддит
USER_AGENT     = "telegram-bot:v0.1 (by /u/Disastrous-Swan6729)"
def search_reddit_images(query: str, limit: int = 50) -> list[str]:
    headers = {"User-Agent": USER_AGENT}
    params  = {"q": query, "limit": limit, "include_over_18": "off", "sort": "relevance", "spoiler": "off"}
    url     = "https://www.reddit.com/search.json"
    resp    = requests.get(url, headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    posts = resp.json().get("data", {}).get("children", [])
    images = []
    for post in posts:
        data = post.get("data", {})
        if data.get("post_hint") == "image" and data.get("url"):
            images.append(data["url"])
    return images

#32кредита
points_by_chat = defaultdict(lambda: defaultdict(int))
CUSTOM_STEPS = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
PRICES = {"beer":  10, "wine":  50, "water": 1,}
ITEM_NAMES = {"beer": "ПИВО", "wine": "ВИНО", "water": "ВОДУ"}

#32кредита
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

#слэш_айди
awaiting_id: dict[int, asyncio.Task] = {}
async def timeout_wait(user_id: int):
    await asyncio.sleep(300)
    if user_id in awaiting_id:
        awaiting_id.pop(user_id)
        try:
            await bot.send_message(user_id, "время вышло крч")
        except Exception:
            pass

#ПРИВЕЕЕЕЕЕЕЕЕЕЕт
GREETINGS = ["Всем доброго утра!", "Доброе утро, друзья!", "Добрейшего утра!", "рыба", "Боброго утра!", "Бобрео!", "Доброго ранку!", "Good morning!", "Всем привет!", "Всем приветики!", "Всем приветулечки!", "صباح الخير!", "Приветствую всех!", "Всем привет, друзья!", "Доброго утречка всем!", "Доброго привета всем!"]

#Айдишки (я швиряю)
VOICEMATUK = "AwACAgIAAyEFAASOMTUcAAENTBdpD4RU_IdBbUx8uu9acjpOlu1imwACrY4AAnQ5eEv_v7fLN6aCijYE"
BOYBOY = "CAACAgIAAxkBAAIkcWjs8pzW92cKSNbUZ6_anJrfhZ2zAAISMwACqF0xSVyTzSbZ_yyGNgQ"
MAX = "CAACAgIAAxkBAAIy42lZLc4o9r-cYd5uPUDkbvu48MpmAALajgACL0vISkofQoFMfkoPOAQ"
LWT_s = "CAACAgIAAyEFAASOMTUcAAEE4NVn9inHavXMCqWPn_cNUEqc-WcEfAACvm0AAjwQIEimtyJLHgP9AjYE"
VSE = "CAACAgIAAyEFAASOMTUcAAEIIshoUyOoUtxdzRpaUHGbbZlCNqKJgAACOVYAAudpgUgFaU4MipFCHDYE"
BEER = ["AgACAgIAAxkBAAIMS2hRh6RFJ97VrO_VenRScZpnczKyAALq9zEbdvaRSiyvahBIp2FHAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMT2hRh7emgSYM0A4UpFbD4MnWvFShAALr9zEbdvaRSqI3juZtZ6aYAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMUWhRh8NAZSrbtCQJOysb7fEL08uXAALs9zEbdvaRSgsKjwPvC_EYAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMWGhRh-hzH8-znxYLgh9_JZrIoo3bAAL39zEbdvaRSnifL2ryXoCgAQADAgADbQADNgQ", "AgACAgIAAxkBAAIMXGhRh_4OUBgsWb-p9bzYQS6rKMngAAL59zEbdvaRSkmhi3EaCU2MAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMYGhRiAoF9sHvU-2KkkCOE7bc26OlAAL69zEbdvaRSlfQkw-W-Sz2AQADAgADeQADNgQ", "AgACAgIAAxkBAAIMaGhRiB-C_hT0TDfaLDHjBN_7nPonAAL79zEbdvaRSsH9PoZUQ_vwAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMbGhRiDELqCPDZA0lJPQvI_hVcIq9AAL89zEbdvaRSmcZKWCEwTbFAQADAgADeAADNgQ"]
WINE = ["AgACAgIAAxkBAAIMcGhRiENNhf4De758uZet5JjRRWrYAAL99zEbdvaRShQ1w9eaqjmDAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMdGhRiFE1iwsBFsF2RXt7jpfn3HSxAAL-9zEbdvaRSuijwHuT-Y6OAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMeGhRiGNK0RDvkE36_AbjjHr_SeDzAAL_9zEbdvaRSqBcd3xVYgi7AQADAgADeAADNgQ", "AgACAgIAAxkBAAIMfGhRiHBC31sZN8ZbixVvq7xAXTWaAAP4MRt29pFK-i1Pgvi-vF8BAAMCAANtAAM2BA", "AgACAgIAAxkBAAIMgGhRiH_5IRUXz4j0eRIx7TxETaChAAIB-DEbdvaRSn5BFxUueK1lAQADAgADeQADNgQ"]
WATER = ["AgACAgIAAxkBAAIMhGhRiJPX_OXCzOGzLbxf4ZaTzBWAAAIC-DEbdvaRSjxxEV7xME0WAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMiGhRiLH2RG3_KIrVM3jCvh98A-TIAAID-DEbdvaRSk43nICK7gABsQEAAwIAA3gAAzYE", "AgACAgIAAxkBAAIMjGhRiNn7e0rCfqYPgr9sMm0oeZ8TAAIE-DEbdvaRSgldbK04OMRDAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMkGhRiOEBbB6ug16i2O8RPp_TptrfAAIF-DEbdvaRSioXVleWVTudAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMlGhRiOvMFVifO8A8IwYdNY1RBgABRAACB_gxG3b2kUr-IqtLv1IrrAEAAwIAA3kAAzYE", "AgACAgIAAxkBAAIMmGhRiPNSnLOsY33kHqd-4CYnr7XlAAII-DEbdvaRSoA_-nLkq2qpAQADAgADeQADNgQ", "AgACAgIAAxkBAAIMnGhRiPwRgRENLCZUTICtg_wmTZ8bAAIJ-DEbdvaRStgpbPu3flz0AQADAgADeQADNgQ", "AgACAgIAAxkBAAIMoGhRiQczRumxwis0z1Pd5EgUdRHKAAIK-DEbdvaRSszUtdoutEqEAQADAgADeAADNgQ", "AgACAgIAAxkBAAIMpGhRiREWLhCbGiMT3WJUdl4pJO-LAAIL-DEbdvaRSmPLHE-kW2BTAQADAgADeQADNgQ"]
VTRI = "AgACAgIAAyEFAASOMTUcAAELyPloxp8_8mzx1EzPD1H8AVsUEJP8cwACTPgxG19bOUo4KlhRhVgeHgEAAwIAA3gAAzYE"

#айдишки (я вижу)
VOROO = "AgADVXMAAtKqMUs"

# че задали? муравей
MURA = "CAACAgIAAxkBAAIkI2jqorXAlw9LHSiFH0RuuXOBrOmpAAIaAAPy6LAmfmdy1pU2dIY2BA"
VEI = "AgADGgAD8uiwJg"
CHEZ = "CAACAgIAAxkBAAIkJ2jqo2RGUI59cq6Lm1ndTDi_4dfeAALFAAPy6LAm7aiTn2lurTU2BA"
ADALI = "AgADxQAD8uiwJg"
















### КОМАНДЫ БОТА
async def start(message: types.Message, args: str):
    await message.answer("эта команда ничего не делает кроме этого сообщения, прикинь")

async def spawnpoint(message: types.Message, args: str):
    await message.answer("Спавнпоинт ПОСТАВЛЕН")

async def admin(message: types.Message, args: str):
    if random.random() < 0.0003619:
        await message.answer("Ты реально считаешь, что команда работает? =/")

async def gm(message: types.Message, args: str):
    messages = ["ОгэПоМониторингу Утра!", "Понятного утра!", "Беспалевного утра!", "Ботпуутра!", "Майнер Крафтового утра!", "ПРАЗДНИЧНОГО ЛИСЬГО УТРЕЧКА", "Интернетного утра!", "Яишницоого утра!", "Борисового утра!", "Выключательного утра!", "Брутального утра!","Водного утра!", "Утренного добреца!", "Киношного утра!", "Диско утра!", "Порхающего утра!", "Липтонового утра!", "Творческого утра!", "Доброе утро блин", "Кошачьего утра!", "Шашлыкового утра!", "Лопухного утра!", "Модераторного утра!", "Админовского утра!", "Мониторного утра!", "Юбилейного утра!", "Наушникового утра!", "Шуточного утра!", "Конфетного утра!", "Стаканного утра!", "Пировогово утра!", "Воро утра!", "Лучшего утра!", "Важного утра!", "Пенопластового утра!", "Картофельного утра!", "Доброе утро!", "Саламандрового утра!", "Утреного добра!", "Боброго утра!", "Бобрео!", "Бобреро!", "Добрейшего утра!", "Крафтового утра!"]
    await message.reply(random.choice(messages))

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

async def motherlode(message: types.Message, args: str):
    return await message.answer(f"блин Бармен спалил эту команду и запретил её =( грустно")
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.full_name
    points_by_chat[chat_id][user_id] += 50000
    await message.answer(f"{username} заюзал чит, бойтесь его")

async def pointy(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    total = points_by_chat[chat_id][user_id]
    await message.reply(f"У вас сейчас {format_cups(total)}")

async def shop(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💧 Вода — 1 кубок", callback_data="buy:water")],
        [InlineKeyboardButton(text="🍺 Пиво — 10 кубков", callback_data="buy:beer")],
        [InlineKeyboardButton(text="🍷 Вино — 50 кубков", callback_data="buy:wine")],
    ])
    await message.answer("прошлый магазин закрылся, поэтому пишу с нового магазина, название не скажу, что желаете купить?", reply_markup=keyboard)
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

async def id(message: types.Message, args: str):
    if message.chat.type != "private":
        return
    user_id = message.from_user.id
    if user_id in awaiting_id:
        awaiting_id[user_id].cancel()
    task = asyncio.create_task(timeout_wait(user_id))
    awaiting_id[user_id] = task
    await message.answer("давай, шли медию мне")
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

async def rr40(message: types.Message, args: str):
    if message.from_user.id != ADMIN_ID:
        return
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

async def wts(message: types.Message, args: str):
    menu_body = format_menu_text(RANDSTICK)
    html = (
        "Выбери конкретную тему:"
        + "<blockquote expandable>"
        + menu_body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        + "</blockquote>"
        + "Либо случайную тему: /rs"
    )
    await message.reply(html, parse_mode=ParseMode.HTML)

async def rs(message: types.Message, args: str):
    topic = random.choice(list(RANDSTICK.keys()))
    pack = random.choice(RANDSTICK[topic])
    sticker_set = await bot.get_sticker_set(name=pack)
    allowed = [s for s in sticker_set.stickers if s.file_unique_id not in BAD]
    if not allowed:
        return await message.reply("во те на те стикеры в квадрате все стикеры с матюками")
    sticker = random.choice(allowed)
    await message.answer_sticker(sticker.file_id)

async def mirror(message: types.Message, args: str):
    if message.date < BOT_START or message.chat.id != CHAT_ID:
        return
    global lab
    if lab:
        lab = False
        return await message.reply("ВОТ НИКОГДА НЕ ПОВЕРИШЬ ШО ПРОИЗОШЛО")
    lab = True
    await message.reply("здесь ооооооооооооооочень длинный текст ну который блин не вмещается ес босс")

async def oda(message: types.Message, args: str):
    if message.date < BOT_START or message.chat.id != CHAT_ID:
        return
    global ODA
    if message.from_user.id != ADMIN_ID:
        return await message.reply("многотексталюишь?любилб")
    if ODA:
        ODA = False
        return await message.reply("вы успокоили аллаха")
    ODA = True
    await message.reply("ТУМБОЧКУ ВРУБИЛИ ЗАЧЕМ")


def now_utc(): return datetime.now(TZ)
def form(n: int, forms: tuple[str,str,str]) -> str:
    n_abs = abs(n)
    if n_abs % 10 == 1 and n_abs % 100 != 11:
        f = forms[0]
    elif n_abs % 10 in (2,3,4) and not (12 <= n_abs % 100 <= 14):
        f = forms[1]
    else:
        f = forms[2]
    return f"{n} {f}"

def split_td(td: timedelta):
    s = int(abs(td).total_seconds())
    d, r = divmod(s, 86400)
    h, r = divmod(r, 3600)
    m, sec = divmod(r, 60)
    return d, h, m, sec

def split_gb(td: timedelta):
    s = int(abs(td).total_seconds())
    h, r = divmod(s, 3600)
    m, sec = divmod(r, 60)
    return h, m, sec

async def kogda(message: types.Message, args: str):
    if message.date < BOT_START or message.chat.id != CHAT_ID:
        return
    return await message.reply("никогда")
    now = datetime.now(MSK)
    if TARGET >= now:
        prefix = "До"
        td = TARGET - now
    else:
        prefix = "От"
        td = now - TARGET
    if TARGET1 >= now:
        prefix1 = "До"
        td1 = TARGET1 - now
    else:
        prefix1 = "От"
        td1 = now - TARGET1
    d,h,m,s = split_td(td)
    d1,h1,m1,s1 = split_td(td1)
    parts = (
        form(d, ("день","дня","дней")),
        form(h, ("час","часа","часов")),
        form(m, ("минута","минуты","минут")),
        form(s, ("секунда","секунды","секунд")),
    )
    parts1 = (
        form(d1, ("день","дня","дней")),
        form(h1, ("час","часа","часов")),
        form(m1, ("минута","минуты","минут")),
        form(s1, ("секунда","секунды","секунд")),
    )
    verb = "осталось" if prefix == "До" else "прошло"
    verb1 = "осталось" if prefix1 == "До" else "прошло"
    await message.reply(f"{prefix} БФДИЕ 2 {verb} {parts[0]}, {parts[1]}, {parts[2]} и {parts[3]}\n{prefix1} дня рождения Джанкила Д, Джанкила {verb1} {parts1[0]}, {parts1[1]}, {parts1[2]} и {parts1[3]}", parse_mode="Markdown")

async def лвк(message: types.Message, args: str):
    if message.date < BOT_START or message.chat.id != CHAT_ID:
        return
    return await message.reply("ЛВК нету ща")
    global LWK
    NAPADENIE = [
        "1. Лемони - 1",
        "2. Пикуда - 2",
        "3. Cross - 7",
        "4. Джанкил Д, - 10",
        "5. Майнер Крафтов - 8",
        "6. Скамптон Велики - 10",
        "7. Монитор - 9",
        "8. tim32.coc - ",
        "9. Воро1 - 11",
        "10. Воро2 - 12",
        "11. XIX Voro XIX -",
        "12. Мониторинг - ",
        "13. Воро3 - 13",
        "14. Воро4 - 14",
        "15. Воро5 - 15",
    ]
    now = datetime.now(MSK)
    if now >= LWK:
        LWK += timedelta(days=1)
    delta = LWK - now
    h,m,s = split_gb(delta)
    parts = (
        form(h, ("час","часа","часов")),
        form(m, ("минута","минуты","минут")),
        form(s, ("секунда","секунды","секунд")),
    )
    inner = "\n".join(html.escape(s) for s in NAPADENIE)
    await message.reply(f"ЛВК закончится через {parts[0]}, {parts[1]} и {parts[2]}.\nСписок нападений ЛВК:\n<blockquote expandable>{inner}</blockquote>\nЗаметки: КК пустые", parse_mode=ParseMode.HTML)

def elochki(txt):
    derevo = re.findall(r'(\d+)🌲', txt)
    zoloto = re.findall(r'(\d+)🎄', txt)
    vse_derevo = sum(int(num) for num in derevo)
    vse_zoloto = sum(int(num) for num in zoloto)
    return vse_derevo, vse_zoloto
farmim = ["🌲", "🎄", None]
chancim = [9, 1, 90]
count = 20
elkiii = defaultdict(lambda: defaultdict(int))
zolotie = defaultdict(lambda: defaultdict(int))

async def farm(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    pick = random.choices(farmim, weights=chancim, k=count)
    result = [p for p in pick if p is not None]
    result_str = "".join(result) or "НИ ОДНОЙ ЁЛКИ блин"
    derevo = result_str.count('🌲')
    elkiii[chat_id][user_id] += derevo
    zoloto = result_str.count('🎄')
    zolotie[chat_id][user_id] += zoloto
    await message.answer(f"ФАРМИМ ЁЛКИ!\n\nВот твои ёлки: {result_str}")

async def elka(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    derevo = elkiii[chat_id][user_id]
    zoloto = zolotie[chat_id][user_id]
    await message.reply(f"У тебя столько ёлок:\n{derevo}🌲\n{zoloto}🎄")

async def sellelki(message: types.Message, args: str):
    if message.date < BOT_START:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    query = message.text.removeprefix("/sellelki ")
    derevo_sell, zoloto_sell = elochki(query)
    if derevo_sell == 0 and zoloto_sell == 0:
        return await message.reply("впиши так: /sellelki X🌲 Y🎄")
    derevo = elkiii[chat_id][user_id]
    zoloto = zolotie[chat_id][user_id]
    total = points_by_chat[chat_id][user_id]
    dengi = 0
    if derevo_sell > derevo:
        return await message.reply("ты чо у тебя мало ёлок")
    if zoloto_sell > zoloto:
        return await message.reply("ты чо у тебя мало золотых ёлок")
    dengi = dengi + derevo_sell
    dengi = dengi + (zoloto_sell*10)
    total = total + dengi
    derevo = derevo - derevo_sell
    zoloto = zoloto - zoloto_sell
    await message.reply(f"Вы продали {derevo_sell} 🌲 и {zoloto_sell} 🎄, получив взамен {format_cups(dengi)}\nСейчас у вас {derevo} 🌲, {zoloto} 🎄 и {format_cups(total)}")
    points_by_chat[chat_id][user_id] = total
    elkiii[chat_id][user_id] = derevo
    zolotie[chat_id][user_id] = zoloto

async def like(message: types.Message, args: str):
    if not message.reply_to_message:
        return
    success = await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
        reaction=[{"type": "emoji", "emoji": "👍"}]
    )

async def nolike(message: types.Message, args: str):
    if not message.reply_to_message:
        return
    success = await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
        reaction=[]
    )

async def pokapoka(message: types.Message, args: str):
    if not message.from_user or message.from_user.id != ADMIN_ID:
        return await message.reply("ты не прав")
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

async def pont(message: types.Message, args: str):
    filfil = message.reply_to_message.photo[-1].file_id
    fileda = await bot.get_file(filfil)
    buffer = BytesIO()
    await bot.download_file(fileda.file_path, buffer)
    buffer.seek(0)
    kartinka = Image.open(buffer)
    okidoki = kartinka.convert("RGB")
    text = message.text.removeprefix("/pont").strip()
#    text = "понтяно"
    draw = ImageDraw.Draw(okidoki)
    rx, ry = okidoki.size
    lobster = ImageFont.truetype("Lobster.ttf", (rx+ry)/20)
    x = rx/2
    y = ry*0.92
    draw.text((x, y), text, font=lobster, anchor="mm", fill =(255, 255, 255))
    okidoki.save("ogogo.png")
    await message.reply_photo(photo=types.FSInputFile("ogogo.png"))

async def pontyano(message: types.Message, args: str):
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

async def write(message: types.Message, args: str):
    global WRITE
    if message.from_user.id != ADMIN_ID:
        return await message.reply("нет, ты не можешь")
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply(f"Нужен АЙДИ\n\nНадо что-то поменять в жизни")
    try:
        m = str(parts[1])
        if m == "Пикуда" or m == "1":
            was = WRITE
            WRITE = 5513644023
            return await message.reply(f"Вроде всё сработало... Старый айди был {was}, теперь он {WRITE}")
        if m == "ОТ" or m == "2":
            was = WRITE
            WRITE = -1002385589532
            return await message.reply(f"Вроде всё сработало... Старый айди был {was}, теперь он {WRITE}")
        if m == "Ковинок" or m == "3":
            was = WRITE
            WRITE = -1003258766039
            return await message.reply(f"Вроде всё сработало... Старый айди был {was}, теперь он {WRITE}")
        m = int(parts[1])
        if m < 99999999999999:
            was = WRITE
            WRITE = m
            return await message.reply(f"Вроде всё сработало... Старый айди был {was}, теперь он {WRITE}")
    except ValueError:
        return await message.reply(f"Нужен АЙДИ\n\nНадо что-то поменять в жизни. И вообще произошёл валю еррор")

async def text(message: types.Message, args: str):
    global TEXT, WRITE
    if message.from_user.id != ADMIN_ID:
        return await message.reply("нет, ты не можешь")
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply(f"Нужен ТЕКСТ\n\nНадо что-то поменять в жизни")
    m = str(parts[1])
    was = TEXT
    TEXT = m
    NAME = await bot.get_chat(WRITE)
    chat = NAME.title or NAME.full_name
    await bot.send_message(WRITE, m)
    return await message.reply(f"Я написала в [{chat}]: {m}")

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

async def rv1(message: types.Message, args: str):
    query = message.text.removeprefix("/rv").strip()
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
    return await message.reply_animation(video_url)
    await message.reply(f"запятая 2")
    for quality in ["tiny", "small", "medium"]:
        url = choice.get(quality, {}).get("url", "")
        if url:
            video_url = url.replace("http://", "https://")
            try:
                return await message.reply_video(video_url)
            except Exception as e:
                return await message.reply(f"ошибка почти кританула: {e}")
    await message.reply("Видео ДОЛЖНО было быть, но что-то пошло не так, как всегда")

OKAY = True
CODIK = defaultdict(lambda: defaultdict(bool))

async def okay(message: types.Message, args: str):
    global OKAY
    if message.from_user.id != ADMIN_ID:
        return
    if OKAY:
        OKAY = False
        return await message.reply("Не окей так не окей")
    OKAY = True
    await message.reply("Окей")

ISTO: dict[int, asyncio.Task] = {}
async def CHASIKI(user_id: int):
    await asyncio.sleep(6000)
    if user_id in ISTO:
        ISTO.pop(user_id)
        try:
            await bot.send_message(user_id, "Слишком долго думаешь! Пиши снова!")
        except Exception:
            pass


async def got(message: types.Message, args: str):
    global CODIK
    chat_id = message.chat.id
    user_id = message.from_user.id
    if CODIK[chat_id][user_id] == True:
        return await message.answer("Да всё, ты решил задачку, молодец")
    if user_id not in ISTO:
        return await message.reply("тебе откуда знать")
    if points_by_chat[chat_id][user_id] == 0:
        return await message.reply("Ты собираешься добывать мне золото или как?")
    if points_by_chat[chat_id][user_id] < 100:
        return await message.reply("кхммммм, думаю золота недостаточно.")
    points_by_chat[chat_id][user_id] -= 100
    await message.reply(f"Во! теперь золота достаточно! Молодец!\nЧасть моего пароля: ILL40SMCAE")
    CODIK[chat_id][user_id] = True
    return ISTO.pop(user_id)


async def фанатпостоянеуходи(message: types.Message, args: str):
    if message.chat.type != "private":
        return await message.answer("Ну не на публике же! ☹️")
    if not OKAY:
        return await message.answer("Бармен пока не дал мне согласия помогать тебе =/")
    chat_id = message.chat.id
    user_id = message.from_user.id
    key = (chat_id, user_id)
    if CODIK[chat_id][user_id] == True:
        return await message.answer("Да всё, ты решил задачку, молодец")
    if user_id in ISTO:
        return await message.answer("Зачем ты снова это пишешь? ☹️")
    task = asyncio.create_task(CHASIKI(user_id))
    ISTO[user_id] = task
    await message.answer("Привет! Ты дошёл до второго этапа моего задания! Чтобы я смогла дать тебе часть пароля, мне нужно, чтобы ты мне помог. У меня есть свой завод по плавке золотых кирок, и возникла проблема: закончилось всё золото! Мне нужно, чтобы ты раздобыл мне золота. Примерно 500 кг золота. Как раздобудешь, уведоми меня командой /got!")






























### РАБОТА БОТА
@dp.message()
async def vse(message: Message):
### ВКЛЮЧИТЬ ВЫКЛЮЧИТЬ БОТА
    global bot_enabled, RANDSTICK
    if message.text:
        if message.date < BOT_START:
            pass
        if message.text.lower() == "иди спать, майнер крафтов":
            if not bot_enabled:
                return
            if message.from_user.id != ADMIN_ID:
                await message.reply("не пойду я спать не хочу")
                return
            await asyncio.sleep(4)
            if not bot_enabled:
                pass
            bot_enabled = False
            await message.reply("хорошо, иду спать, всем спокойного сна")
        if message.text.lower() == "просыпайся, майнер крафтов":
            if bot_enabled:
                return
            if message.from_user.id != ADMIN_ID:
                await message.reply("не хочу я просыпаться не мешай мне спать")
                return
            await asyncio.sleep(4)
            if bot_enabled:
                return
            bot_enabled = True
            await message.reply("доброго утра всем! 😀")
            return
    if not bot_enabled:
        return
    if message.from_user.id == HURMO and ODA:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
### ШАНСЫ
    if message.chat.id == CHAT_ID:
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
### ШТУКИ В КОМАНДНОЙ СТРОКЕ
    chat = message.chat.title or message.from_user.full_name
    username = message.from_user.full_name
    emoji = getattr(message.sticker, "emoji", None)
    content = f"{emoji + ' ' if emoji else ''}{'[' + message.content_type.removeprefix("ContentType.") + '] ' if not message.text else ''}{message.caption or message.text if message.caption or message.text else ''}"
    print(f"[{chat}]\n{username}: {content}")
### А ТАК МОЖНО ЧТОЛИ
    RANDSTICK = {
    "monitor": ["Monitornosti", "monitoringmiku", "monitoringdeco"],
    "v": ["VGoddessDronDronV_by_fStikBot", "vsoocute_by_SozdaiStickeriBot", "v_md_by_fStikBot", "v_murderdrones_by_fStikBot", "V_Murder_Drones_by_fStikBot", "vmurderdrones", "v_murder_drones"],
    "fox": ["foxanulis_by_TgEmodziBot", "Foxeshere_by_fStikBot", "foxfox", "foxfoxfox", "foxfoxfoxfoxfox", "foxes_by_fStikBot", "fox_core_by_fStikBot", "Ilovefoxes", "i_love_foxes", "i_love_fox", "ilovefoxes_by_fStikBot", "ilovefox_by_TgEmodziBot"],
    "voro": ["ArmiyaVorony", "Voronuuuuuuuu_by_fStikBot", "crowcrow_by_fStikBot"],
    "leafy": ["LeafyWaving", "LEAFYBFBstatic", "leafy_bfb_bfdi2_by_fStikBot", "LEAFY_CUTE_XD", "t6211125a_fd71_4b84_92d2_6c2688a84053_by_emopix_stickerz_bot", "Peko_Lifi_Lifi", "Peko_Lifi", "leafy_bfb_bfdi_by_fStikBot", "leafybfb", "leafybfb_by_fStikBot", "leafy_bfb"],
    "firey": ["Spotless_Beige_Guan_by_fStikBot", "FireyBlueberrySticker_by_fStikBot", "fireybfdi", "FIREYBFDI_by_fStikBot", "firey_bfb_by_fStikBot"],
    "two": ["TwoBfdi_Tpot", "twotpot"],
    "barmen": ["Barmen_40"],
    "cyberfoxy": ["CyberFoxy_by_TgEmodziBot"],
    "dandy": ["bc517e3b_a078_4f59_92ba_8e0a9df026a1_by_sticat_bot", "BobettCore", "veestickersdandysworld_by_fStikBot", "bobettedandyworld", "bobettedandyworld_by_fStikBot", "gourdy", "GourdyDandyWorld", "gourdy_by_fStikBot"],
    "pvz": ["pvz_2_m", "winter_melon"],
    "teto": ["Tetocore", "tetotetotetoteto", "teto_core", "iloveteto", "tetotetoteto_by_fStikBot", "tetotetotetoteto_by_fStikBot", "tetotetotetotetoteto_by_fStikBot", "iloveteto_by_fStikBot", "teto_by_TgEmodziBot", "TetoTetoTeto_by_TgEmodziBot", "tetotetotetotetotetoteto_by_TgEmodziBot"],
    "scampton": ["Sjkabwisnhwkwbdspamton", "SpriteV2UndertaleDeltaruneStickers_by_fStikBot", "Skamti_by_fStikBot", "scamptonthegreat", "scampton_by_fStikBot", "scampton_by_TgEmodziBot", "scampton_the_great"],
    "45": ["Sigma1454", "OtvechatelskijRazum"],
    "bear": ["GlamrockFreddy_Dad_by_fStikBot", "GlamrockFreddyEarth928B"],
    "bobr": ["beaver1952_by_TgEmodziBot", "Naideno_v_Yandeks_Kartinkakh_po_zaprosu_bobyor_iz_kr_by_fStikBot", "BobrBobr_by_TgEmodziBot"],
    "jimo": ["AdeptusMechahanicus"],
    "pon": ["AIEIVYASNT_by_stikeri_stikeri_bot", "monkeypon", "monkepon", "monkeypon_by_fStikBot", "monkey_pon_by_fStikBot", "monkepon_by_fStikBot", "monkepon_by_TgEmodziBot"],
    "skelet": ["skeletopack_by_fStikBot", "DevelopedStoat_by_fStikBot", "krytueskelet_by_fStikBot", "Manyskeletons_by_fStikBot", "GENCANAYOO", "iloveskeletons", "skeletonskeleton", "iloveskeleton_by_fStikBot"],
    "lomat": ["EduardoLaloSalamanca", "lalosalamanca", "nachovarga_by_fStikBot", "lalo_salamanca", "tucosalamanca", "tuco_salamanca", "lalonachogay_by_fStikBot", "breabad_by_fStikBot", "BBBCSECLanaDemova_by_fStikBot", "Saul_goodman", "Saul_by_fStikBot"],
    "cow": ["kolxozkoriva_by_fStikBot", "ilovecows", "cows_by_fStikBot"]
    }
### КОМАНДЫ
    if message.chat.id != CHAT_ID:
        outout = ("voro", "leafy", "firey", "two", "dandy", "bobr", "jimo", "pon", "skelet", "lomat", "cow")
        REALLYOUT = {k: RANDSTICK[k] for k in outout}
        RANDSTICK = REALLYOUT
    if message.text and message.text.startswith("/"):
        parts = message.text.split(maxsplit=1)
        cmd_with_slash = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cmd = cmd_with_slash.lstrip("/").split("@", 1)[0].lower()
        if cmd in RANDSTICK:
            pack_list = RANDSTICK.get(cmd, [])
            if not pack_list:
                return await message.reply("э а где стикеры")
            chosen = random.choice(pack_list)
            sticker_set = await bot.get_sticker_set(name=chosen)
            allowed = [s for s in sticker_set.stickers if s.file_unique_id not in BAD]
            if not allowed:
                return await message.reply("вот те на те стикеры с матюками")
            sticker = random.choice(allowed)
            await message.answer_sticker(sticker.file_id)
        func = getattr(sys.modules[__name__], cmd, None)
        if func and inspect.iscoroutinefunction(func):
            await func(message, args)
        return
    if message.date < BOT_START:
        return
### ЗЕРКАЛО
    if lab and message.chat.id == CHAT_ID:
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
    if message.text:
### Целый текст
        if message.from_user.id == JUNKR and ODA:
            await message.reply("*здесь злой текст о том, что Джанкил должен ~~отправится за игру в форсакен~~ отправиться кодить*")
        if message.text.lower() == "кейн, купи пиво":
            await message.answer("Кейн, купи пиво")
        if message.text.lower() == "я вернулся" and message.chat.id == CHAT_ID:
            await message.answer_sticker(sticker=MAX)
        if message.text.lower() == "кобо":
            await message.answer("Справді гуманізований розумний голос")
        if message.text.lower() == "муравей" and message.chat.id == CHAT_ID:
            await message.reply_sticker(sticker=CHEZ)
        if message.text.lower() == "че задали" and message.chat.id == CHAT_ID:
            await message.reply_sticker(sticker=MURA)
        if message.text.lower() == "воро":
            await message.answer("Воро")
### Слова в тексте
        if "2763" in message.text.lower() and message.chat.id == CHAT_ID:
            await message.reply_sticker(sticker=LWT_s)
        elif "27:63" in message.text.lower() and message.chat.id == CHAT_ID:
            await message.reply_sticker(sticker=LWT_s)
        if "все" in message.text.lower() and message.chat.id == CHAT_ID and random.random() < 0.01:
            await message.reply_sticker(sticker=VSE)
        if "майнера крафтов" in message.text.lower():
            await message.reply("не зли меня, бяка >=(")
    if message.sticker:
        if message.sticker.file_unique_id == VOROO:
            await message.reply("Воро")
        if message.sticker.file_unique_id == VEI:
            await message.reply_sticker(sticker=CHEZ)
        if message.sticker.file_unique_id == ADALI:
            await message.reply_sticker(sticker=MURA)













### БУДИЛЬНИКИ

async def vtrin():
    global bot_enabled
    now = datetime.now(MSK)
    await bot.send_message(ADMIN_ID, "доброе утро!")
    if 7 <= now.hour < 13:
        await bot.send_message(CHAT_ID, random.choice(GREETINGS))
    while True:
        now = datetime.now(MSK)
        if now.hour == 13 and now.minute == 56:
            await bot.send_photo(CHAT_ID, photo=VTRI)
            await asyncio.sleep(61)
        await asyncio.sleep(5)
        if now.hour == 19 and now.minute == 52:
            await bot.send_message(CHAT_ID, "📻📻📻")
            await asyncio.sleep(61)
        await asyncio.sleep(5)


### ТЕКСТ В КОМАНДНОЙ СТРОКЕ

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
    stickers = [s for s in set_.stickers if s.file_unique_id not in BAD]
    if not stickers:
        print(f"У {pack} МАТЮЮЮЮЮЮЮЮЮЮЮЮК")
        return
    sticker = random.choice(stickers)
    await bot.send_sticker(WRITE, sticker=sticker.file_id)
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
        if line.startswith("/"):  # команда
            cmd = line[1:].split("@", 1)[0]  # /cats@bot -> cats
            await send_sticker(cmd)
        else:
            try:
                await bot.send_message(chat_id=WRITE, text=line)
                print("Швирнула... а шо швирнула?")
            except Exception as e:
                print("не хочу отправлять вот Опричнина:", e)

#запись и запуск бота
async def main():
#    logging.basicConfig(level=logging.INFO)
#    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=False),
        console_sender(),
        vtrin()
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
        print("я спать пошла, спокойной ночи")
