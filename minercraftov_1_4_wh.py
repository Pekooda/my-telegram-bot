#### ВЕРСИИ:
# 1.0 - релиз бота
# 1.1 - фикс багов
# 1.2 - релиз создания стикерпаков
# 1.3 - шкала ярости и орлюки, поддержка базы данных, короче всё всё всё
# 1.4 - подготовка к деплою, стабилизация /rp /rv /ttm
# 1.4.wh - вебхук

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, logging, random, re, requests, html, os, json, ffmpeg, subprocess, math, aiohttp, io
from aiohttp import web
from PIL import ImageFont
from io import BytesIO
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, Update, ChatPermissions, FSInputFile, BufferedInputFile
from aiogram.types.input_sticker import InputSticker
from aiogram.filters import Command
from aiogram.enums import ParseMode
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
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

chest = {
    "NUMB": 301,
    "kazn": {
        "st": {
            "NAME": "Гнев Разрушения",
            "PRICE": 1,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "в течении минуты я изничтожу все гифки/стикеры Тима",
            "TYPE": "time"
        },
        "lv": {
            "NAME": "Гнев Поглощения",
            "PRICE": 3,
            "VALUE": 2,
            "NOW": 0,
            "INFO": "в течении 2 минут я буду поглощать гифки/стикеры Тима, поглощая в дополнительные минуты гнева",
            "TYPE": "time"
        },
        "sk": {
            "NAME": "Гнев Превращения",
            "PRICE": 2,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "в течении минуты я буду превращать гифки/стикеры Тима в случайные стикеры",
            "TYPE": "time"
        },
        "ob": {
            "NAME": "Гнев Уничтожения",
            "PRICE": 3,
            "VALUE": 1,
            "NOW": 0,
            "INFO": "я уничтожу следующую гифку/стикер Тима",
            "TYPE": "use"
        }
    },
    "GIFTIM": {
        "AgAD_wIAAkAaTVM": {
            "VALUE": 6,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIYGGmzQQHPAgWqKJtA5w_SrKSSRz3sAAL_AgACQBpNU76nd4Ed73pIOgQ"
        },
        "AgADDQMAAiRStVM": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJXmGnGOb6m77v8iYHgecKc5kN4MggAAw0DAAIkUrVTGdFTisiT_4U6BA"
        },
        "AgAD6gUAAjFZNVA": {
            "VALUE": 2,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJTXWnEDfnh25Unrjqd_LyYx4y4yogtAALqBQACMVk1UJICjh6hEx8UOgQ"
        },
        "AgADWQYAAvJQ_FE": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIbg2m0DHXKEBQ6Ff0tnS42WX4FnAuSAAJZBgAC8lD8UbImUZBCEg3xOgQ"
        },
        "AgAD6IoAAl6kKUk": {
            "VALUE": 12,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJdsWnI6th4V-NsISq7RzYzPdCb2BxGAALoigACXqQpSebzr8UAAUaDDToE"
        },
        "AgADtgIAAnXUDFM": {
            "VALUE": 6,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJWvGnGMzy4x4gAAXtTCP85QGDOobnDzQACtgIAAnXUDFNukzARZ695AjoE"
        },
        "AgADHgMAAqCfDFM": {
            "VALUE": 28,
            "WHAT": "Гифка с бегающим мейн боссом 4 главы андертейл",
            "GIF": "CgACAgQAAyEFAATCPNLXAAEDButpw3kGu1Y3U-SKuBLbNX5K022QbgACHgMAAqCfDFMW-1zBQBd4gDoE"
        },
        "AgADOwYAAiIHxVM": {
            "VALUE": 3,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJX5WnGV0bdSk39oUwHEeKoSiCo-bK5AAI7BgACIgfFUyw80zxHCif-OgQ"
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
        "AgAD8AIAAkkNDVM": {
            "VALUE": 7,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJZPmnGzx4xVULZH3qKFDTEVG5xDBq9AALwAgACSQ0NU4VbzP5zv4fDOgQ"
        },
        "AgADnwIAAl3UDFM": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATCPNLXAAEDO_1pzBbdl86mFh_SVRZQEgL8dNF2EAACnwIAAl3UDFNsuGfrbP0PFjoE"
        },
        "AgADQwgAAkPxLVI": {
            "VALUE": 21,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJRsWnDxjI4DYV6nmJ-QZuC42IzaeVQAAJDCAACQ_EtUpWjDEWPVVvuOgQ"
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
            "VALUE": 30,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJStmnD-elbCBubVpB-wIfK3eiVd_lGAAJSCAACFM0tUuwhw0IvN-XzOgQ"
        },
        "AgADaAMAAtjXhFA": {
            "VALUE": 11,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJZdGnG4b2LpuAZWxm8Xa4dAvKtrAzxAAJoAwAC2NeEUJjJF6rWpl3oOgQ"
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
            "VALUE": 9,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJTY2nEDgv0m7Qk1cNgy39uWUcL4_0QAAJQBAACSkUFUL_DwHdMVuAhOgQ"
        },
        "AgAD4oYAAkn94Es": {
            "VALUE": 1,
            "GIF": "CAACAgIAAxkBAAJUm2m0sOvP68PR01o7wIY95bklraJAAALihgACSf3gS19wykz3h-oFOgQ"
        },
        "AgADUQQAAnSelFM": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAIx2Gm5fRttMl-i6cyS8PLnp4aCjallAAJRBAACdJ6UU5nGRIMzzHDyOgQ"
        },
        "AgADBAMAAkhwDFM": {
            "VALUE": 2,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJPh2nC0N1RhkbV7bFrWXQ_MuoXD6IdAAIEAwACSHAMU8JG3gM3Avq2OgQ"
        },
        "AgAD9nAAAnFAWEs": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATmi0vRAAJRuWnDxpddznoUV6aSyeY5L8_dGt43AAL2cAACcUBYS9tl95CsAAHbQToE"
        },
        "AgADFJoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTi2nEFIdTfVvS5hdRgIPU95qgXnP-AAIUmgACYOEgSlwaPmS05lhrOgQ"
        },
        "AgADFpoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTjGnEFIe_1mBK-UIofayISh7jaxToAAIWmgACYOEgSjavybetSWyoOgQ"
        },
        "AgADF5oAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTjWnEFIig7r0jLA8ysDYObJZsM1syAAIXmgACYOEgSlhOpRYESU9KOgQ"
        },
        "AgADGJoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTjmnEFIhiUDUbF1vA7W_eRA3aoKrEAAIYmgACYOEgSrp81D-DU6A-OgQ"
        },
        "AgADGZoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTj2nEFIlyRrEGJBZsi1B_DUyKnDZjAAIZmgACYOEgSl_W5F1CnsELOgQ"
        },
        "AgADaZoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTnGnEGFrErjn7EpY3CgTFn9U4h6gKAAJpmgACYOEgSmQMPgrKNXWnOgQ"
        },
        "AgADapoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTnWnEGGLZgf1kW6cBMZ65PQoYWGlnAAJqmgACYOEgSmt2VjEwxJUIOgQ"
        },
        "AgADa5oAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTnmnEGGJSbGZYq9Umd6dzBBTIxFlPAAJrmgACYOEgSpyMBPomz8A5OgQ"
        },
        "AgADbJoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJTn2nEGGP9bohm5uGtOxqR4k23AewXAAJsmgACYOEgSjlugrI7nTWeOgQ"
        },
        "AgADbZoAAmDhIEo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJToGnEGGNXgFcAARE27F8uqjn5l0gq5QACbZoAAmDhIEoWsrXK0vMdijoE"
        },
        "AgADKwcAAqxvJFA": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJX4WnGVtWcQYIsCiDxUJqGGFN9Yu94AAIrBwACrG8kUANmBsEhk901OgQ"
        },
        "AgAD6QIAApoIDFM": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJYE2nGWTj4fFbJJcq1qFqmUiQGN1eVAALpAgACmggMUzln_uf0yyFwOgQ"
        },
        "AgAD1QkAAnR5VVA": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJYRGnGWyyJ3of-R3eHmkPtR3s6eHjXAALVCQACdHlVUI4PYejoNoHlOgQ"
        },
        "AgADowcAAsY2nVA": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJYSGnGWzwTPhwRBiUw5pNQlqxMoGcJAAKjBwACxjadUDZ9xSPKMiLAOgQ"
        },
        "AgADHgcAAsCshVE": {
            "VALUE": 4,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJYYGnGZfQT66VU_qJY2ObJhKStd28FAAIeBwACwKyFUWWTVGDtz64_OgQ"
        },
        "AgADCgcAAhgFdVM": {
            "VALUE": 2,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJYbGnGbWleYeQ2wNmwB8-Vwb5e2UKKAAIKBwACGAV1U7M8UQlrK_NlOgQ"
        },
        "AgAD8AUAAiy2ZFE": {
            "VALUE": 5,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJZG2nGw3C59viirR_t8UfPXhGFq7bKAALwBQACLLZkUVrifCh99jJ7OgQ"
        },
        "AgAD6wIAApBpDVM": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJZZ2nG4MB621k4WkePmW5PwlswrLGfAALrAgACkGkNU_PjAqv3RdPWOgQ"
        },
        "AgADbwgAAsNhjVI": {
            "VALUE": 1,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJcB2nIAAHIqhQKegvuhBD0PhSW67zsMgACbwgAAsNhjVIHvDlBQTPs-DoE"
        },
        "AgADfgcAAs-OvFI": {
            "VALUE": 2,
            "GIF": "CgACAgQAAyEFAATmi0vRAAJcCWnIAAHSvaPVb-5Ekkuy3NLtqW5HRgACfgcAAs-OvFJCEgABuc_BlRY6BA"
        },
        "AgADKX8AApzGwEk": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJcDGnIAAH0-1ZTEozjfANlZTg2NvQpeAACKX8AApzGwEmCAdVhMIrQajoE"
        },
        "AgADK38AApzGwEk": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJcEGnIAR4G3HrINiYjJtjrkYdp1rd7AAIrfwACnMbASUa1LZpe6mWTOgQ"
        },
        "AgADU5kAAvIGQUo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJcEmnIAVLrnRPHn4xP3WseJDj4wT_sAAJTmQAC8gZBSjaB6ALeeQo7OgQ"
        },
        "AgADVJkAAvIGQUo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJcE2nIAW0_GsnUiGXKbGBIq5vIAxCMAAJUmQAC8gZBSvBCzVUKUxR5OgQ"
        },
        "AgADVZkAAvIGQUo": {
            "VALUE": 1,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJcFGnIAYJL-vpoUJAKRM5MrS-F-2twAAJVmQAC8gZBSmKGU1hQeMIDOgQ"
        },
        "AgADOBgAAoPAsEo": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATmi0vRAAJYYWnGZiNu1iTwODX7tyuao8VUoLx_AAI4GAACg8CwSqVPSLqF0GmsOgQ"
        },
        "AgADnZAAAuyoQEk": {
            "VALUE": 1,
            "GIF": "CAACAgIAAyEFAATCPNLXAAEDO65pzBFxQM2gcZ4jeTROcHwzQWEhGwACnZAAAuyoQEkOSe81fSUdijoE"
        },
        "AgADraUAAiUeaEo": {
            "VALUE": 3,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJjg2nNGauh_HAW6wv9qU7PgYrqtwABKgACraUAAiUeaEqICkba8vKmCjoE"
        },
        "AgADs6UAAiUeaEo": {
            "VALUE": 5,
            "GIF": "CgACAgIAAyEFAATmi0vRAAJjhGnNGeZzrKo_daDqTuZS_bWm_uzAAAKzpQACJR5oShIge3kr-fkcOgQ"
        }
    },
    "rich": {
        "5513644023": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "-1003258766039": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "-1003867888593": {
            "lab": False,
            "cmh": False,
            "cmt": False
        }
    }
}


### ДАТАБАЗА
def openchest():
    global chest
    return chest
def closechest(chestto):
    global chest
    chest = chestto

def nozerolast(parts, numb):
    if len(parts) > numb:
        COUNT = int(parts[numb])
    else:
        return 1
    if COUNT < 1 or not parts[numb].lstrip("-").isdigit():
        return 0
    return COUNT




























#### КОМАНДЫ БОТА
### Начало жизни
async def start(message: types.Message, args: str):
    await message.answer(f"Я работаю. Меня запустили в {MSKnow}.")


### Достать датабазу
async def data(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return
    chest = openchest()
    text = json.dumps(chest, indent=4, ensure_ascii=False).replace("true", "True").replace("false", "False")
    file = BufferedInputFile(
        text.encode("utf-8"),
        filename="chest.json"
    )
    await message.answer_document(file)


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


### МАТЕМАТИКА
mgcheck: dict[int, asyncio.Task] = {}
async def math_waiting(user_id: int):
    await asyncio.sleep(10)
    if user_id in mgcheck:
        mgcheck.pop(user_id)
        try:
            await bot.send_message(user_id, "время вышло крч")
        except Exception:
            pass
answera = defaultdict(int)
async def mathgame(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    d1 = random.randint(1, 100)
    d2 = random.randint(1, 100)
    dz = random.choice(["+", "-"])
    de = str(d1) + dz + str(d2)
    desc = f"""
Математика!
В течении 10 секунд реши следующее уравнение:
{de}
"""
    global answera
    answera[user_id] = eval(de)
    await message.reply(desc)
    task = asyncio.create_task(math_waiting(user_id, chat_id))
    mgcheck[user_id] = task
@dp.message(lambda message: message.from_user.id in mgcheck)
async def answeris(message: Message):
    user_id = message.from_user.id
    if message.text.lower() == str(answera[user_id]):
        task = mgcheck.pop(user_id)
        task.cancel()
        await message.reply("Верно! Молодец!")
    else:
        await message.reply("Неверно.")
async def mathi(message: types.Message, args: str):
    user_id = message.from_user.id
    await mathgame(message)


### Рычаги
async def richagi(message: types.Message, args: str, cmd_name: str):
    if (cmd_name == "cmt" and message.from_user.id == TIM_ID) or (cmd_name == "cmh" and message.from_user.id == HURM_ID):
        return await message.reply("Неа.")
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


### Случайные картинки/видео
## Проверка на матюк
def MATUK_CHECK(text):
    for w in MATUUUK:
        pattern = rf"^{re.escape(w)}\w*"
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False

## Рандом на "орлюк"
async def orluk(message: types.Message, args: str):
    query = "орел"
    tes = random.choice([rv, rp])
    eagle = await tes(message, query)
    if tes == rp:
        await message.answer_photo(eagle)
    else:
        await message.answer_animation(eagle)

## Человек написал или кто
def queryfilter(message, query, com):
    R = message.text.startswith(f"/{com}")
    texting = query.split()
    maxpage = 200
    if len(texting) > 0 and texting[0].startswith("-") and texting[0].lstrip("-").isdigit():
        if int(texting[0].lstrip("-")) < 3:
            page = 3
        elif int(texting[0].lstrip("-")) < maxpage:
            page = int(texting[0].lstrip("-"))
        else:
            page = maxpage
        query = query.lstrip(texting[0]).strip()
    else:
        page = maxpage
    if message.reply_to_message:
        query = message.reply_to_message.text or ""
    if not query:
        query = random.choice(DEFAULT_QUERY)
    return R, query, page

## НЕ НЕЙРОНИТЬ ПЛИЗ
def noaipls(hits):
    bad_tokens = ("ai", "neural", "ai-art", "ai_generated", "aiart", "нейросеть", "нейро", "ии", "искусственный интеллект")
    filtered = []
    for h in hits:
        klu = []
        for key in ["tags", "page", "user", "alt"]:
            keyk = h.get(key)
            if not isinstance(keyk, str):
                continue
            klu.append(keyk)
        if any(bt in str(klu).lower() for bt in bad_tokens):
            continue
        filtered.append(h)
    return filtered

## Много, поэтому
def thingforpexel(query):
    texting = query.split()
    maxpage = 80
    if len(texting) > 0 and texting[0].startswith("-") and texting[0].lstrip("-").isdigit():
        if int(texting[0].lstrip("-")) < 1:
            page = 1
        elif int(texting[0].lstrip("-")) < maxpage:
            page = int(texting[0].lstrip("-"))
        else:
            page = maxpage
        query = query.lstrip(texting[0]).strip()
    else:
        page = maxpage
    if bool(re.search(r'[\u0400-\u04FF]', query)):
        lang = "ru-RU"
    else:
        lang = "en-US"
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": page, "locale": lang}
    return key, params

## Генератор случайных картинок
async def rp(message: types.Message, quer: str):
    query = quer
    RP, query, page = queryfilter(message, query, "rp")
    params = {"key": PIXABAY_KEY, "q": query, "image_type": "photo", "safesearch": "true", "per_page": page}
    try:
        resp = requests.get("https://pixabay.com/api/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception as e:
        hits = False
        pass
    if not hits:
        key, params = thingforpexel(quer)
        try:
            resp = requests.get("https://api.pexels.com/v1/search", params=params, headers=key, timeout=5)
            data = resp.json()
            hits = data.get("photos", [])
        except Exception as e:
            return False, await message.reply("ошибка кританула: {e}")
        if not hits:
            return False, await message.reply(f"Я ничего не нашла эх блин")
    filtered = noaipls(hits)
    pool = filtered or hits
    choice = random.choice(pool)
    img_url = choice.get("webformatURL") or choice["src"]["large"]
    if RP:
        await message.answer_photo(img_url)
    else:
        return query, img_url

## Генератор случайных видео
async def rv(message: types.Message, quer: str):
    query = quer
    RV, query, page = queryfilter(message, query, "rv")
    params = {"key": PIXABAY_KEY, "q": query, "video_type": "all", "per_page": page}
    try:
        resp = requests.get("https://pixabay.com/api/videos/", params=params, timeout=5)
        data = resp.json()
        hits = data.get("hits", [])
    except Exception:
        pass
    if not hits:
        key, params = thingforpexel(quer)
        try:
            resp = requests.get("https://api.pexels.com/videos/search", params=params, headers=key, timeout=5)
            data = resp.json()
            hits = data.get("videos", [])
        except Exception as e:
            return False, await message.reply(f"ошибка кританула: {e}")
        if not hits:
            return False, await message.reply("Я ничего не нашла эх блин")
    filtered = noaipls(hits)
    pool = filtered or hits
    choice = random.choice(pool)
    video_data = choice.get("videos", {})
    for quality in ["tiny", "small", "medium"]:
        url = video_data.get(quality, {}).get("url", "") or choice["video_files"][0]["link"]
        if url:
            video_url = url.replace("http://", "https://")
            if RV:
                return await message.answer_animation(video_url)
            else:
                return query, video_url


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
        width = ImageFont.truetype(font, maxsize).getlength(pon)
        if width <= maxwid:
            break
        maxsize -= 1
    imfont = ImageFont.truetype(font, maxsize)
    return pon, imfont, maxsize


async def ttm(message: types.Message, args: str):
    buffer = BytesIO()
    rep = message.reply_to_message or message
    media = rep.photo[-1] if rep.photo else rep.animation or rep.sticker or rep.video
    args = (args if len(args) > 0 else message.reply_to_message.text or args) if message.reply_to_message else args
    texting = args.split()
    args = args.removeprefix("-v ")
    if not args:
        args = random.choice(DEFAULT_QUERY)
    if media and not (rep.sticker and rep.sticker.is_animated):
        x = media.width
        y = media.height
        pic = await bot.get_file(media.file_id)
        isvideo = False
        istgs = False
        if rep.photo:
            forma = "png"
        elif rep.sticker:
            forma = "webp"
        elif rep.sticker and rep.sticker.is_video:
            forma = "webm"
        elif rep.animation or rep.video:
            forma = "mp4"
            isvideo = True
        infile = f"/tmp/aco.{forma}"
        outfile = f"/tmp/line.{forma}"
        infilewebp = infile.replace("{forma}", "webp")
        infilemp4 = infile.replace("{forma}", "mp4")
        await bot.download_file(pic.file_path, infile)
    else:
        if len(texting) > 0 and texting[0] == "-v":
            ran = rv
            forma = "mp4"
            isvideo = True
        else:
            ran = rp
            forma = "png"
            isvideo = False
        infile = f"/tmp/aco.{forma}"
        outfile = f"/tmp/line.{forma}"
        pic, htp = await ran(message, args)
        if not pic:
            return
        else:
            args = pic
        async with aiohttp.ClientSession() as session:
            async with session.get(htp) as resp:
                if resp.status != 200:
                    return await message.answer("No download ;(")
                with open(infile, "wb") as f:
                    f.write(await resp.read())
        ohno = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", infile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        info = json.loads(ohno.stdout)
        x = info["streams"][0]["width"]
        y = info["streams"][0]["height"]
    if rep.sticker and rep.sticker.is_video and not texting[0] == "-v":
        ohno = subprocess.run(
            ["ffmpeg", "-i", infile, "-vframes", "1", "-vf", infilewebp],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        forma = "webp"
        os.remove(infile)
        infile = infilewebp
    elif rep.sticker and rep.sticker.is_video and texting[0] == "-v":
        ohno = subprocess.run(
            ["ffmpeg", "-i", infile, infilemp4],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        args = args.lstrip("-v ")
        forma = "mp4"
        os.remove(infile)
        infile = infilemp4
    font = "Lobster.ttf"
    size = min(x, y)/10
    mlt = 80*(x/y)
    mwt = x*0.9
    mina = x/100
    outl = x/150
    textout, fontout, sizeout = textstab(x, y, args.lower(), mlt, mwt, size, font, mina)
    textout = textout.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
    comas = ["ffmpeg", "-y", "-i", infile, "-vf", f"drawtext=fontfile={font}:text='{textout}':x=(w-text_w)/2:y=(h-text_h)/2+h*0.8/2:fontsize={sizeout}:fontcolor=white:borderw='{outl}':bordercolor=black"]
    if isvideo:
        comas += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-an"]
    comas += [outfile]
    ohno = subprocess.run(
        comas,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    try:
        if forma in ["webm", "webp"]:
            await message.answer_sticker(FSInputFile(outfile))
        if forma == "mp4":
            await message.answer_animation(FSInputFile(outfile))
        if forma == "png":
            await message.answer_photo(FSInputFile(outfile))
    except Exception as e:
        if str(e) == "Telegram server says - Bad Request: file must be non-empty":
            await message.answer(f"Я не всегда могу наносить текст на текст, надо другой стикер :/")
        else:
            await message.answer(f"Probla: {e}")
    os.remove(infile)
    os.remove(outfile)


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
        return
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
        return
    chest = openchest()
    for key in chest["kazn"]:
        chest["kazn"][key]["NOW"] = 0
    closechest(chest)
    await message.answer(f"Хорошо, я его пощадила... но...")

## Покупка гнева
async def gnev(message: types.Message, args: str):
    if message.from_user.id == TIM_ID:
        return await message.answer(f"неа")
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
        "-ot": OT_ID, # ОТ
        "-cov": COVINOC_ID, # КОВИНОК
        "-otold": OTOLD_ID, # ОТ_OLD
        "-peko": PEKO_ID # ПИКУДА
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
### ШАНСЫ
    if message.chat.id == OT_ID and random.random() < 0.0003619: 
        if random.random() < 0.01:
            await message.reply("ГИГАСЛУЖЕБНОЕ СООБЩЕНИЕ БОГОВ ОЛИМПУСА, 1 к 276300!!!!!")
        elif random.random() < 0.1: 
            await message.reply("НАСТОЛЬКО СЛУЖЕБНОЕ СООБЩЕНИЕ, ЧТО ПИПЕЦ, 1 к 27630")
        else:
            await message.reply("СЛУЖЕБНОЕ СООБЩЕНИЕ")
### КОНСОЛЬ
    print(f"[{message.chat.title or message.from_user.full_name}]\n{message.from_user.full_name}: {getattr(message.sticker, "emoji", None) + ' ' if getattr(message.sticker, "emoji", None) else ''}{'[' + message.content_type.removeprefix("ContentType.") + '] ' if not message.text else ''}{message.caption or message.text if message.caption or message.text else ''}")



### ВСЁ, ЧТО НИЖЕ - НЕ ОТПРАВИТСЯ ПРИ ЗАПУСКЕ
    if message.date < BOT_START:
        return
### Мгновенная реакция
    if message.from_user.id == TIM_ID and chest["rich"][f"{chat_id}"]["cmt"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["cmh"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)


### ЗАПИСЬ ЧАТА В ДЖСОН
    if f"{chat_id}" not in chest["rich"]:
        chest["rich"][f"{chat_id}"] = {
            "lab": False,
            "cmh": False,
            "cmt": False
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
        capor = message.text or message.caption
        parts = capor.split(maxsplit=1)
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
        original = ""
        if message.caption:
            original = message.caption.replace(".", ",")
        if message.text:
            original = message.text.replace(".", ",")
            await bot.send_message(chat_id=chat_id, text=original)
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
        media = message.photo[-1] if message.photo else message.animation or message.sticker or message.video or message.voice or message.document or message.file
        file_id = media.file_id
        unique_id = media.file_unique_id
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
                await rs(message, "")
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
















#### БУДИЛЬНИКИ
async def alarms():
### Сообщение админу о включении
    await bot.send_message(PEKO_ID, random.choice(GREETINGS))
    print(f"о я здесь но писать уже нельзя, а то\n")
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
        chest = openchest()
        for i in range(60):
            await asyncio.sleep(60)
            for key in chest["kazn"]:
                if chest["kazn"][key]["TYPE"] == "time":
                    chest["kazn"][key]["NOW"] = max(0, chest["kazn"][key]["NOW"] - 1)
            closechest(chest)
        if chest["NUMB"] > 0:
            chest["NUMB"] -= 1
            closechest(chest)

        













async def pingser():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=5) as resp:
                    if resp.status == 429:
                        logging.debug("RATE LIMIT! sleeping longer...")
                        await asyncio.sleep(300)
                    else:
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
    logging.debug("=== STARTED ===")
    app["task1"] = asyncio.create_task(alarms())
    app["task2"] = asyncio.create_task(pivtime())
    app["task3"] = asyncio.create_task(pingser())
async def on_cleanup(app):
    for name in ["task1", "task2", "task3"]:
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