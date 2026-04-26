#### ВЕРСИИ:
# 1.0 - релиз бота
# 1.1 - фикс багов
# 1.2 - релиз создания стикерпаков
# 1.3 - шкала ярости и орлюки, поддержка базы данных, короче всё всё всё
# 1.4 - подготовка к деплою, стабилизация /rp /rv /ttm
# 1.5 - вру, сейчас
# 1.6 - что-то то, что не сказано

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ
import asyncio, logging, random, re, requests, html, os, json, ffmpeg, subprocess, math, aiohttp, io
from PIL import ImageFont
from io import BytesIO
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, Update, ChatPermissions, FSInputFile, BufferedInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from aiohttp import web

### КЛЮЧИКИ АЙДИШКИ (СЕКРЕТНО!)
load_dotenv()
TOKEN_KEY = os.getenv("E_TOKEN_KEY")
PIXABAY_KEY = os.getenv("E_PIXABAY_KEY")
PEXELS_KEY = os.getenv("E_PEXELS_KEY")
REDDIT_KEY = os.getenv("E_REDDIT_KEY")
MY_CHEST = os.getenv("E_MY_CHEST")
URL = os.getenv("E_URL_KEY")
URL_TWO = os.getenv("E_URL_KEY_TWO")
PEKO_ID = int(os.getenv("E_PEKO_ID"), 0)
JUNK_ID = int(os.getenv("E_JUNK_ID"), 0)
OT_ID = int(os.getenv("E_OT_ID"), 0)
OTOLD_ID = int(os.getenv("E_OTOLD_ID"), 0)
COVINOC_ID = int(os.getenv("E_COVINOC_ID"), 0)
HURM_ID = int(os.getenv("E_HURM_ID"), 0)
TIM_ID = int(os.getenv("E_TIM_ID"), 0)
ISCRA_ID = int(os.getenv("E_ISCRA_ID"), 0)
MATUUUK = json.loads(os.getenv("E_MATUUUK", "[]"))
FUL_MATUUUK = json.loads(os.getenv("E_FUL_MATUUUK", "[]"))

### ПЕРЕМЕННЫЕ
bot = Bot(token=TOKEN_KEY)
dp = Dispatcher()
TZ = timezone.utc
BOT_START = datetime.now(TZ)
MSK = timezone(timedelta(hours=3))
MSKnow = datetime.now(MSK)
bot_enabled = True
mediaidcheck = defaultdict(int)
mgcheck: dict[int, asyncio.Task] = {}
answera = defaultdict(int)


### ХЛАМ
comasiv = ["start", "guide", "data", "admin", "gm", "id", "like", "nolike", "mathi", "wts", "rs", "orluk", "rp", "rv", "ttm", "pong", "mercy", "gnev", "makaka", "pokapoka", "text", "rr40", "hmer", "hkazn"]
MC_NAME = ["майнер крафтов", "мк"]
DEFAULT_QUERY = ["пиво", "пиво"]
MURA_NIQ = "CAACAgIAAxkBAAIkI2jqorXAlw9LHSiFH0RuuXOBrOmpAAIaAAPy6LAmfmdy1pU2dIY2BA"
CHEZ_NIQ = "CAACAgIAAxkBAAIkJ2jqo2RGUI59cq6Lm1ndTDi_4dfeAALFAAPy6LAm7aiTn2lurTU2BA"
MAX_NIQ = "CAACAgIAAxkBAAIy42lZLc4o9r-cYd5uPUDkbvu48MpmAALajgACL0vISkofQoFMfkoPOAQ"
LEAFY_NIQ = "CAACAgIAAyEFAASOMTUcAAEE4NVn9inHavXMCqWPn_cNUEqc-WcEfAACvm0AAjwQIEimtyJLHgP9AjYE"
VSE_NIQ = "CAACAgIAAyEFAASOMTUcAAEIIshoUyOoUtxdzRpaUHGbbZlCNqKJgAACOVYAAudpgUgFaU4MipFCHDYE"
VTRI_NIQ = "AgACAgIAAyEFAASOMTUcAAELyPloxp8_8mzx1EzPD1H8AVsUEJP8cwACTPgxG19bOUo4KlhRhVgeHgEAAwIAA3gAAzYE"
VORO_UIQ = "AgADVXMAAtKqMUs"
CRO_UIQ = "AgAD1pkAAgir8Ug"
VEI_UIQ = "AgADGgAD8uiwJg"
ADALI_UIQ = "AgADxQAD8uiwJg"
colorit = ["grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown", "violet"]
langa = ["cs", "da", "de", "en", "es", "fr", "id", "it", "hu", "nl", "no", "pl", "pt", "ro", "sk", "fi", "sv", "tr", "vi", "th", "bg", "ru", "el", "ja", "ko", "zh"]


GREETINGS = ["Всем доброго утра!", "Доброе утро, друзья!", "Добрейшего утра!", "рыба", "Боброго утра!", "Бобрео!", "Доброго ранку!", "Good morning!", "Всем привет!", "Всем приветики!", "Всем приветулечки!", "صباح الخير!", "Приветствую всех!", "Всем привет, друзья!", "Доброго утречка всем!", "Доброго привета всем!", "ОгэПоМониторингу Утра!", "Понятного утра!", "Беспалевного утра!", "Ботпуутра!", "Майнер Крафтового утра!", "ПРАЗДНИЧНОГО ЛИСЬГО УТРЕЧКА", "Интернетного утра!", "Яишницоого утра!", "Борисового утра!", "Выключательного утра!", "Брутального утра!","Водного утра!", "Утренного добреца!", "Киношного утра!", "Диско утра!", "Порхающего утра!", "Липтонового утра!", "Творческого утра!", "Доброе утро блин", "Кошачьего утра!", "Шашлыкового утра!", "Лопухного утра!", "Модераторного утра!", "Админовского утра!", "Мониторного утра!", "Юбилейного утра!", "Наушникового утра!", "Шуточного утра!", "Конфетного утра!", "Стаканного утра!", "Пировогово утра!", "Воро утра!", "Лучшего утра!", "Важного утра!", "Пенопластового утра!", "Картофельного утра!", "Доброе утро!", "Саламандрового утра!", "Утреного добра!", "Бобреро!", "Добрейшего утра!", "Крафтового утра!", "Нового утра!", "Утра, которого ещё никогда не было!", "Освежающего утра!", "Хеллоуинского утра!", "Страшного утра!", "Вампиршеского утра!", "Существующего утра!", "А ГДЕ утра!", "СКАААААЙПового утра!", "Самого нужного утра!"]


chest = {
    "hurma": {
        "hurmball": 20,
        "hurmcd": False
    },
    "stick": {
        "monitor": [
            "Monitornosti",
            "monitoringmiku",
            "monitoringdeco"
        ],
        "v": [
            "VGoddessDronDronV_by_fStikBot",
            "vsoocute_by_SozdaiStickeriBot",
            "v_md_by_fStikBot",
            "v_murderdrones_by_fStikBot",
            "V_Murder_Drones_by_fStikBot",
            "vmurderdrones",
            "v_murder_drones"
        ],
        "fox": [
            "foxanulis_by_TgEmodziBot",
            "Foxeshere_by_fStikBot",
            "foxfox",
            "foxfoxfox",
            "foxfoxfoxfoxfox",
            "foxes_by_fStikBot",
            "fox_core_by_fStikBot",
            "Ilovefoxes",
            "i_love_foxes",
            "i_love_fox",
            "ilovefoxes_by_fStikBot",
            "ilovefox_by_TgEmodziBot"
        ],
        "voro": [
            "ArmiyaVorony",
            "Voronuuuuuuuu_by_fStikBot",
            "crowcrow_by_fStikBot"
        ],
        "pivo": [
            "ukrainianbeer_by_fStikBot",
            "XenophobicTanSilkworm_by_fStikBot",
            "pivopivopivopivo228",
            "o3ZtvWu_by_sticker2004Bot",
            "MedovoePivO_by_fStikBot",
            "Ipman2",
            "PivoUltimate"
        ],
        "leafy": [
            "LEAFYBFBstatic",
            "leafy_bfb_bfdi2_by_fStikBot",
            "LEAFY_CUTE_XD",
            "t6211125a_fd71_4b84_92d2_6c2688a84053_by_emopix_stickerz_bot",
            "Peko_Lifi_Lifi",
            "Peko_Lifi",
            "leafy_bfb_bfdi_by_fStikBot",
            "leafybfb",
            "leafybfb_by_fStikBot",
            "leafy_bfb"
        ],
        "firey": [
            "Spotless_Beige_Guan_by_fStikBot",
            "FireyBlueberrySticker_by_fStikBot",
            "fireybfdi",
            "FIREYBFDI_by_fStikBot",
            "firey_bfb_by_fStikBot"
        ],
        "two": [
            "TwoBfdi_Tpot",
            "twotpot"
        ],
        "barmen": [
            "Barmen_40"
        ],
        "cyberfoxy": [
            "CyberFoxy_by_TgEmodziBot"
        ],
        "dandy": [
            "bc517e3b_a078_4f59_92ba_8e0a9df026a1_by_sticat_bot",
            "BobettCore",
            "veestickersdandysworld_by_fStikBot",
            "bobettedandyworld",
            "bobettedandyworld_by_fStikBot",
            "gourdy",
            "GourdyDandyWorld",
            "gourdy_by_fStikBot"
        ],
        "pvz": [
            "pvz_2_m",
            "winter_melon"
        ],
        "teto": [
            "Tetocore",
            "tetotetotetoteto",
            "teto_core",
            "iloveteto",
            "tetotetoteto_by_fStikBot",
            "tetotetotetoteto_by_fStikBot",
            "tetotetotetotetoteto_by_fStikBot",
            "iloveteto_by_fStikBot",
            "teto_by_TgEmodziBot",
            "TetoTetoTeto_by_TgEmodziBot",
            "tetotetotetotetotetoteto_by_TgEmodziBot"
        ],
        "scampton": [
            "Sjkabwisnhwkwbdspamton",
            "SpriteV2UndertaleDeltaruneStickers_by_fStikBot",
            "Skamti_by_fStikBot",
            "scamptonthegreat",
            "scampton_by_fStikBot",
            "scampton_by_TgEmodziBot",
            "scampton_the_great"
        ],
        "45": [
            "Sigma1454",
            "OtvechatelskijRazum"
        ],
        "bear": [
            "GlamrockFreddy_Dad_by_fStikBot",
            "GlamrockFreddyEarth928B"
        ],
        "bobr": [
            "beaver1952_by_TgEmodziBot",
            "Naideno_v_Yandeks_Kartinkakh_po_zaprosu_bobyor_iz_kr_by_fStikBot",
            "BobrBobr_by_TgEmodziBot"
        ],
        "jimo": [
            "AdeptusMechahanicus"
        ],
        "pon": [
            "AIEIVYASNT_by_stikeri_stikeri_bot",
            "monkeypon",
            "monkepon",
            "monkeypon_by_fStikBot",
            "monkey_pon_by_fStikBot",
            "monkepon_by_fStikBot",
            "monkepon_by_TgEmodziBot"
        ],
        "skelet": [
            "skeletopack_by_fStikBot",
            "DevelopedStoat_by_fStikBot",
            "krytueskelet_by_fStikBot",
            "Manyskeletons_by_fStikBot",
            "GENCANAYOO",
            "iloveskeletons",
            "skeletonskeleton",
            "iloveskeleton_by_fStikBot"
        ],
        "lomat": [
            "EduardoLaloSalamanca",
            "lalosalamanca",
            "nachovarga_by_fStikBot",
            "lalo_salamanca",
            "tucosalamanca",
            "tuco_salamanca",
            "lalonachogay_by_fStikBot",
            "breabad_by_fStikBot",
            "BBBCSECLanaDemova_by_fStikBot",
            "Saul_goodman",
            "Saul_by_fStikBot"
        ],
        "jevil": [
            "JevilV2UndertaleDeltaruneStickers_by_fStikBot",
            "jevil_sticksundertale",
            "Jevil23",
            "PoS_Jevil",
            "Jevil199",
            "JevilTheJester_by_fStikBot",
            "Dzhevil14",
            "pk_2325279_by_Ctikerubot"
        ],
        "mtt": [
            "hard_drive_2_by_fStikBot",
            "Mettaton_HardDrive",
            "mettatton"
        ],
        "cow": [
            "kolxozkoriva_by_fStikBot",
            "ilovecows",
            "cows_by_fStikBot"
        ],
        "figli": [
            "prequel_memes",
            "swpre2"
        ],
        "tim": [
            "otvechatelskayatroica",
            "blablalablala40_by_minercraftov_bot",
            "timmakakaslampochkoi_by_tgemodzibot",
            "otvechalovo_tim"
        ]
    },
    "badstick": [
        "AgADoAcAApXm4UY",
        "AgADQxQAAuzDuUg",
        "AgADXRYAAg7iQUg",
        "AgADKxgAAogoSUg",
        "AgAD6REAAvONSEg",
        "AgADxhcAAimBQUg",
        "AgADbBYAAnyieEs",
        "AgADcRcAAvixeUs",
        "AgADYBMAAphCeUs",
        "AgADnxMAArCJeUs",
        "AgADHhMAAgxeeUs",
        "AgADLhYAAlmNeEs",
        "AgADkhYAAnIfeUs",
        "AgADJwAD-5IlBg",
        "AgAD6DwAApI1wEg",
        "AgAD0DsAAvFJwEg",
        "AgADB0EAAmdQwEg",
        "AgADBkQAAgdiwEg",
        "AgADhDwAAjKPyEg",
        "AgADRjoAAsrnwEg",
        "AgADhD0AAqWtwEg",
        "AgADVToAAiF8wUg",
        "AgADkTgAAmqcwEg",
        "AgADRzkAAoQ1wUg",
        "AgADHT4AAg-ewEg",
        "AgADXj0AAmtJwUg",
        "AgADdEEAAr52wUg",
        "AgADfkkAAiJgwEo",
        "AgAD20QAAnjkwEo",
        "AgADwTcAAjE7IEk",
        "AgADkxQAAkFlsEs",
        "AgADBhYAAkZLqEs",
        "AgADFBYAAlmFwEo",
        "AgAD-SMAAr0g2Eg",
        "AgAD5x4AAkA22Eg",
        "AgADiB4AAmdISEg",
        "AgAD0iMAAsNkSEg",
        "AgADhR0AAs5DSEg",
        "AgAD2yIAAneRSUg",
        "AgAD3R4AAstPSUg",
        "AgADYCUAAtVgwUs",
        "AgADCRcAAqmfyUs",
        "AgADSB0AAoUvwEs",
        "AgADcBsAAu_wwEs",
        "AgADKx4AAoFjWEs",
        "AgADohwAA1NYSw",
        "AgADohkAAqEsUUs",
        "AgAD0h8AAvesOEs",
        "AgADrRsAAi_n-Eo",
        "AgADgBkAAiZaeEo",
        "AgADLB0AAnOkwEk",
        "AgADQxoAAj5UyUk",
        "AgADZRYAArUvAAFK",
        "AgADsV0AAstqyUs",
        "AgADFlwAAqp5-Eg",
        "AgADimkAAoSdIEg",
        "AgADMWEAApisSUo",
        "AgAD9mwAAvUYYEo",
        "AgADOmQAAnp98Eg",
        "AgADmGwAAhy6IUk",
        "AgADE1oAAql8OUs",
        "AgAD_G8AAtNrmUo",
        "AgADfwEAAokqwFU",
        "AgADH00AAlXhwUk",
        "AgADT1QAAtMgyUk",
        "AgADpmUAAgUf6Us",
        "AgAD9WAAAneYwUs",
        "AgADRlwAAhhAyUs",
        "AgADngADvo8yGA",
        "AgADhgADvo8yGA",
        "AgADywADvo8yGA",
        "AgADfwADvo8yGA",
        "AgADhAADvo8yGA",
        "AgADsgADvo8yGA",
        "AgADrXkAAlO3kUg",
        "AgADvSgAAlE9wUo",
        "AgADVisAArYSwEo",
        "AgADOCoAAqSOwEo",
        "AgADPyIAAtxtyEo",
        "AgADwSEAAoo5yUo",
        "AgADbSQAAqYiwUo",
        "AgADkCwAAj34wUo",
        "AgADA1sAAs__0Es",
        "AgADFB4AApl6mEs",
        "AgAD6SAAAnX7oUs",
        "AgADEh4AAtYkoUs",
        "AgADEiIAArb5oEs",
        "AgADSiEAAnzeoUs",
        "AgADJSIAAm91mEs",
        "AgADuR4AAhhCmEs",
        "AgADpBsAAqm8oEs",
        "AgADHCAAAq8NmEs",
        "AgAD9x8AAuwRmEs",
        "AgADFiIAAvfsmEs",
        "AgAD9yAAAkDpmUs",
        "AgAD2CIAAor5oUs",
        "AgADcR8AApb6mUs",
        "AgADdiEAAuRfoEs",
        "AgADaCMAAhQLmUs",
        "AgADpR4AAqujmUs",
        "AgADqyEAAjdymEs",
        "AgADeR8AApACmEs",
        "AgADJh4AAgvnmEs",
        "AgADvyIAAtglmEs",
        "AgADwSAAAr-qoUs",
        "AgADCSIAAvKpmUs",
        "AgADUiEAAmyZoEs",
        "AgADsCoAAiyImUs",
        "AgADmCIAAq83mEs",
        "AgADRiUAAoHAmEs",
        "AgADTRsAAnFfmEs",
        "AgADlCAAAoQrmUs",
        "AgADAR8AAnOhoUs",
        "AgADqx8AAgrjmEs",
        "AgADkyAAAtgDmUs",
        "AgADuiEAAqFMmEs",
        "AgADvxwAAsdqoEs",
        "AgADzCAAAkO_oUs",
        "AgADuyUAAjn0oEs",
        "AgADJSIAAho_mUs",
        "AgADUh8AAniwoEs",
        "AgADESAAAmkHmEs",
        "AgADGi0AAoi5oUs",
        "AgADJCIAAiQvoUs",
        "AgADWCIAAqzRoEs",
        "AgAD-BoAArbdmEs",
        "AgADcCAAAqbBmUs",
        "AgADbB4AAqEvoEs",
        "AgADdCIAAmEMoUs",
        "AgADjiIAAgP6oUs",
        "AgADESIAAu-FoUs",
        "AgADxR8AAkobmUs",
        "AgADLB8AAuR3oEs",
        "AgADvh8AAhKooEs",
        "AgADCR4AAgejqUs",
        "AgADgh8AAjjTmUs",
        "AgADSx4AArP-oEs",
        "AgADBD8AAtO9GEg",
        "AgAD-i0AAmtqwUo",
        "AgADvBgAAl6ISUk",
        "AgADdmwAAkyASUo",
        "AgADpWIAAhMEyEs",
        "AgADmTQAAiBHwEk",
        "AgAD0iwAAgQu2Uk",
        "AgADDysAAnbrAUg",
        "AgAD0WcAAtAtSEo",
        "AgADomUAAn2pGUs",
        "AgADq3QAAtu9GUs",
        "AgADw3AAAsr0OEs",
        "AgADpXEAAvsimUs",
        "AgADMmkAAgWZOUo",
        "AgADuWIAAggEOUo",
        "AgADdmwAAkyASUo",
        "AgADgzoAAtOJAUg",
        "AgADSzkAAv3tAUg",
        "AgAD0igAApFL4Eg",
        "AgADCSkAAs_O4Ug",
        "AgAD9SkAAghD4Ug",
        "AgADciUAApi44Eg",
        "AgADRD0AArTgaUo",
        "AgADMUAAAxloSg",
        "AgADcUIAAgtnyUs",
        "AgADL3QAApQ7qUs",
        "AgADcnkAAtsSsUs",
        "AgAD8BoAApVeoUk",
        "AgAD3hsAAqLkmEk",
        "AgAD1nUAAuA3eEk",
        "AgADRUkAAoCZ6Uk",
        "AgADJUYAAjIF6Ek",
        "AgADvkEAAibb8Uk",
        "AgADtkIAApAQMUo",
        "AgADVUEAAuZfMUo",
        "AgADzUEAAntHMUo",
        "AgADBwUAAggtGUQ",
        "AgADqgYAAtN0OEc",
        "AgADpj0AAi--QUo",
        "AgADmBIAAmc1iEk",
        "AgADV1QAAi7fGEg",
        "AgAD0B4AApLNeEk",
        "AgADMRoAAusAAYFJ",
        "AgAD1RwAAhsceUk",
        "AgADghkAAgineUk",
        "AgAD9CkAAlO2iEs",
        "AgADmBsAAo5YiUs",
        "AgADOBsAAmcJ2Uo",
        "AgADZhcAAjRh4Uo",
        "AgADBgQAAkLtJRY",
        "AgADoIEAAtaUiUg",
        "AgADzk4AAt3N2Uk",
        "AgADK1MAAu_52Uk",
        "AgADsHIAAvipkUg",
        "AgADJFkAAtDhAUk",
        "AgADnk0AAhpsCEk",
        "AgADTFAAArzPeEk",
        "AgAD31EAAqiASUk",
        "AgADNlAAAk3iKUo",
        "AgADYBcAAjGXyEo",
        "AgADCBsAAjS6yUo",
        "AgADqRwAAtNY0Uo",
        "AgADYyIAAupZyUo",
        "AgAD8xYAAidlyEo",
        "AgADrhcAAihoyUo",
        "AgADvxgAAm7SyUo",
        "AgADXR8AAmzCyUo",
        "AgADPhwAAvxpyUo",
        "AgADdRgAArvO0Eo",
        "AgADNxkAAn2hyEo",
        "AgADpBsAAuygyUo",
        "AgADCBQAAqvL8Us",
        "AgAD6REAAg6M8Us",
        "AgADchMAAgYc8Us",
        "AgADPxgAAo95-Us",
        "AgADEBcAAos2SUg",
        "AgADvREAAncBsVA",
        "AgADFBAAAq5tsVA",
        "AgADNxgAAvP0sVA",
        "AgADCg4AAkmzsVA",
        "AgADEBIAAvRJsFA",
        "AgAD6g8AApdmsVA",
        "AgADLQ8AAiYYsFA",
        "AgADWQ0AAto2sFA",
        "AgADQiMAAlwLkUk",
        "AgADzx8AApTxkUk",
        "AgADshYAAr04kUk",
        "AgAD-xkAAj8qkEk",
        "AgAD3D8AApuPwEg",
        "AgAD0D0AAiDiwEg",
        "AgAD5DQAAtFQwUg",
        "AgADrjYAAjDHyEg",
        "AgADID4AAkxFwUg",
        "AgADezkAAuOpwUg",
        "AgADkzcAAqGhwUg",
        "AgADsDcAApYxwEg",
        "AgAD5T0AArBZwUg"
    ],
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
        },
        "-1002699937978": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "5566808793": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "6121849328": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "5134703218": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "8535933456": {
            "lab": False,
            "cmh": False,
            "cmt": False
        },
        "8067578447": {
            "lab": False,
            "cmh": False,
            "cmt": False
        }
    },
    "timtim": {
        "timtext": 0,
        "timeout": 1,
        "maxgif": 100,
        "timrep": {
            "AgADUAQAAkpFBVA": {
                "VALUE": 13,
                "ID": "CgACAgQAAyEFAATmi0vRAALALWntvWTzNUWmDkqoenUSDOD3THUmAAJQBAACSkUFUL_DwHdMVuAhOwQ",
                "NAME": "howard-hamlin.mp4",
                "TIME": 1001
            },
            "AgADpwcAAqCq1FA": {
                "VALUE": -98,
                "ID": "CgACAgQAAyEFAATmi0vRAALBA2nt43JhvL3Z1S658tpyj_MSQ-_2AAKnBwACoKrUUJqA8Z7dkub9OwQ",
                "NAME": "vocaloid-monitoring.mp4",
                "TIME": 734
            },
            "AgADQZQAAibRyUo": {
                "VALUE": 6,
                "ID": "CgACAgIAAyEFAATmi0vRAAKYMmnjWob53zYhDxuE86OqTTOPYfZwAAJBlAACJtHJSm48_CeMc_UROwQ",
                "NAME": "bo-sinn-smeshariki.mp4",
                "TIME": 26
            },
            "AgADQwgAAkPxLVI": {
                "VALUE": 10,
                "ID": "CgACAgQAAyEFAATmi0vRAALAJmntvTJ7QJluT2VrZtvNwmTpqFj0AAJDCAACQ_EtUpWjDEWPVVvuOwQ",
                "NAME": "deltarune-deltarune-chapter-3.mp4",
                "TIME": 315
            },
            "AgAD6gUAAjFZNVA": {
                "VALUE": 4,
                "ID": "CgACAgQAAyEFAATmi0vRAALAUmnt0CA5QLV8P9SuKCaHP3RtIN8YAALqBQACMVk1UJICjh6hEx8UOwQ",
                "NAME": "freedom-america.mp4",
                "TIME": 790
            },
            "AgAD6wMAAmOntVE": {
                "VALUE": 5,
                "ID": "CgACAgQAAyEFAATmi0vRAALAFWntpYRQlI_Jdz9RcarpzO__UlSaAALrAwACY6e1UdV8UaoRbLAsOwQ",
                "NAME": "снаступающимновымгодом2023_снаступающимновымгодом.mp4",
                "TIME": 1004
            },
            "AQADKhZrGxBGaUt-": {
                "VALUE": 3,
                "ID": "AgACAgIAAyEFAATmi0vRAALARmntz2t6Fqj0c9YHd6Aa8JTcxwl7AAIqFmsbEEZpS8OdqXxofmi0AQADAgADeQADOwQ",
                "NAME": "Photo",
                "TIME": 621
            },
            "AQADNw5rG_JirFB9": {
                "VALUE": 1,
                "ID": "AgACAgQAAyEFAATmi0vRAALATmntz81ajRhdWRUl4-6GD3nQOyysAAI3Dmsb8mKsUBUCY68h5820AQADAgADeAADOwQ",
                "NAME": "Photo",
                "TIME": 394
            },
            "AQADPBZrGxBGaUt-": {
                "VALUE": 1,
                "ID": "AgACAgIAAyEFAATmi0vRAALAZ2nt0g97Pdx4_Ej0Oya0NOJ1UDReAAI8FmsbEEZpSzjC4nIyBhoHAQADAgADeQADOwQ",
                "NAME": "Photo",
                "TIME": 404
            },
            "AQADWhZrGxBGaUt9": {
                "VALUE": 1,
                "ID": "AgACAgIAAyEFAATmi0vRAALA2Gnt2VpDxx1hzdyON88BjdMO4U5gAAJaFmsbEEZpS11R4bYmtsBDAQADAgADeAADOwQ",
                "NAME": "Photo",
                "TIME": 435
            },
            "AQAD6RRrG018cEt-": {
                "VALUE": 1,
                "ID": "AgACAgIAAyEFAATmi0vRAALCBmnuG9eQjtAPwsIof3-BzsKb1OPaAALpFGsbTXxwS3YWgYmWj0pQAQADAgADeQADOwQ",
                "NAME": "Photo",
                "TIME": 621
            },
            "AQAD3xRrGxBGcUt-": {
                "VALUE": 1,
                "ID": "AgACAgIAAyEFAATmi0vRAALCK2nuHLfX_cdUlV6nfnbrzUoBiP1sAALfFGsbEEZxS0neQGWyKp3wAQADAgADeQADOwQ",
                "NAME": "Photo",
                "TIME": 625
            },
            "AgADWAcAAqf_tVI": {
                "VALUE": 1,
                "ID": "CgACAgQAAyEFAATmi0vRAALDuWnuN83nHhdfrbAMlwJk4a0YY7O9AAJYBwACp_-1UqWHa-X_GPGEOwQ",
                "NAME": "dandy-world-yatta.mp4",
                "TIME": 723
            },
            "AgADN2IAAgPG8Uk": {
                "VALUE": 2,
                "ID": "CgACAgIAAyEFAATmi0vRAALDu2nuN9LTYl11owenY_uwVfdIddU5AAI3YgACA8bxSYah8vuE6zDQOwQ",
                "NAME": "хелоуин.gif.mp4",
                "TIME": 973
            },
            "AgAD6lsAApY0WUs": {
                "VALUE": 1,
                "ID": "CgACAgIAAyEFAATmi0vRAALEVGnuRQ0y4zJjv_FpAZrIwyCRDXgAA-pbAAKWNFlL6lOyjBY8irY7BA",
                "NAME": "GIF",
                "TIME": 779
            },
            "AgADUggAAhTNLVI": {
                "VALUE": 2,
                "ID": "CgACAgQAAyEFAATmi0vRAALF32nuT4cWxi_5lg_WCvYlfPQmNbPxAAJSCAACFM0tUuwhw0IvN-XzOwQ",
                "NAME": "deltarune-deltarune-chapter-3.mp4",
                "TIME": 950
            },
            "AgADpWIAAhMEyEs": {
                "VALUE": 1,
                "ID": "CAACAgIAAyEFAATmi0vRAALHImnub6js02gxm9nnMBYTCKYpK3gqAAKlYgACEwTISx33CYrbAfjIOwQ",
                "NAME": "Sticker 📦",
                "TIME": 961
            },
            "AgADIgYAAuNuOhk": {
                "VALUE": 1,
                "ID": "CAACAgIAAyEFAATmi0vRAALIp2nufAqnHyqEWqj1TQOomrEuNQ5EAAIiBgAC4246GfHxsr2ck0etOwQ",
                "NAME": "Sticker 😐",
                "TIME": 1014
            },
            "AgAD8AIAAkkNDVM": {
                "VALUE": 1,
                "ID": "CgACAgQAAyEFAATmi0vRAALItWnufNbOZam25DsJrSiDtjh8zRS4AALwAgACSQ0NU4VbzP5zv4fDOwQ",
                "NAME": "like.mp4",
                "TIME": 1017
            }
        }
    }
}




### ДАТАБАЗА
def openchest():
    global chest
    return chest
def closechest(chest):
    return






























#### КОМАНДЫ БОТА
### Начало жизни
async def start(message: types.Message, args: str):
    await message.answer(f"Я работаю. Меня запустили в {MSKnow}.")


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
async def math_waiting(message: types.Message):
    await asyncio.sleep(10)
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in mgcheck:
        mgcheck.pop(user_id)
        await message.reply("Вы не успели угадать =Р")
@dp.message(lambda message: message.from_user.id in mgcheck)
async def answeris(message: Message):
    user_id = message.from_user.id
    if message.text and message.text.lower() == str(answera[user_id]):
        task = mgcheck.pop(user_id)
        task.cancel()
        await message.reply("Верно! Молодец!")
    else:
        await message.reply("Неверно.")
async def mathi(message: types.Message, args: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if args == "medium":
        for i in range(10):
            d1 = random.randint(10, 100)
            d2 = random.randint(10, 100)
            d3 = random.randint(2, 10)
            d4 = random.randint(2, 10)
            dz = random.choice(["+", "-"])
            dd1 = random.choice(["*", "/"])
            dd2 = random.choice(["*", "/"])
            de = str(d1) + dd1 + str(d3) + dz + str(d2) + dd2 + str(d4)
            if eval(de) > 1 or eval(de) < -1:
                break
    elif args == "hard":
        for i in range(10):
            d1 = random.randint(10, 100)
            d2 = random.randint(10, 100)
            d3 = random.randint(10, 100)
            dz = random.choice(["*", "/"])
            dd = random.choice(["*", "/"])
            de = str(d1) + dz + str(d2) + dd + str(d3)
            if eval(de) > 1 or eval(de) < -1:
                break
    else:
        d1 = random.randint(10, 100)
        d2 = random.randint(10, 100)
        dz = random.choice(["+", "-"])
        de = str(d1) + dz + str(d2)
    desc = f"""
Математика!
В течении 10 секунд реши следующее уравнение:
{de}
Округление происходит до целого числа
"""
    global answera
    answera[user_id] = math.floor(eval(de) + 0.5)
    await message.reply(desc)
    task = asyncio.create_task(math_waiting(message))
    mgcheck[user_id] = task


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
    chest = openchest()
    if not args or not message.from_user.id == PEKO_ID:
        lines = [""]
        for cmd in chest["stick"].keys():
            lines.append(f"/{cmd}\n")
        menubody = "<blockquote expandable>" + "".join(lines) + "</blockquote>"
        await message.reply(f"""
Выбери конкретную тему:
{menubody}Либо случайную тему: /rs
""", parse_mode="HTML")
    else:
        textong = args.split()
        texting = args.lower().split()
        text = ""
        if texting[len(texting) - 1] != "confirm":
            pass
        elif len(texting) == 3:
            cmdcheck = texting[1] in chest["stick"].keys()
            stcheck = textong[1] in chest["badstick"]
            if texting[0] == "addcmd":
                if not cmdcheck:
                    text = "Команда добавлена"
                    chest["stick"][texting[1]] = []
                else:
                    text = "Команда уже существует"
            elif texting[0] == "delcmd":
                if cmdcheck:
                    text = "Команда удалена"
                    del chest["stick"][texting[1]]
                else:
                    text = "Команды не существует"
            if texting[0] == "goodst":
                if stcheck:
                    text = "Стикер больше не игнорируется"
                    chest["badstick"].remove(textong[1])
                else:
                    text = "Стикера в списке не существует, как и... ихиххихих... Сургута."
        elif len(texting) == 4:
            cmdcheck = texting[2] in chest["stick"].keys()
            stcheck = textong[1] in chest["badstick"]
            if cmdcheck:
                packcheck = texting[1] in chest["stick"][texting[2]]
            if not cmdcheck:
                text = "Команды для этого стикерпака не существует, как и сам знаешь, кого"
            elif texting[0] == "addpack":
                if not packcheck:
                    try:
                        await bot.get_sticker_set(texting[1].lower())
                        text = "Стикерпак добавлен до команды"
                        chest["stick"][texting[2]] += [texting[1]]
                    except Exception as e:
                        text = "Стикерпак не добавлен, поскольку его не существует (Привет, Сургут! xD)"
                else:
                    text = "Стикерпак не добавлен, ибо он уже существует, в отличии от Сургута >=("
            elif texting[0] == "delpack":
                if packcheck:
                    text = "Стикерпак удалён из команды"
                    chest["stick"][texting[2]].remove(texting[1].lower())
                else:
                    text = "Стикерпака в команде не существует, как и Сургута..."
            if texting[0] == "badst":
                if not stcheck:
                    try:
                        await bot.get_file(textong[2])
                        text = "Стикер игнорируется"
                        chest["badstick"] += [textong[1]]
                    except Exception as e:
                        text = f"Стикер не добавлен, поскольку его не существует. Сургуты в шоке: {e}"
                else:
                    text = "Стикер уже наказан за плохое поведение. =|"
        if not text:
            text = f"""Команды:
🔼 addcmd [cmd] - добавить пустую команду для стикерпаков
🔽 delcmd [cmd] - удалить существующую команду для стикерпаков
⏫ addpack [pack] [cmd] - добавить существующий стикерпак до команды для стикерпаков
⏬ delpack [pack] [cmd] - удалить существующий стикерпак с команды для стикерпаков
⭕️ badst [UIQ] [ID] - добавить существующий стикер в список игнорирования
🟢 goodst [UIQ] - удалить существующий стикер из списка игнорирования
    Для выполнения команд выше требуется написать CONFIRM в конце.
Команды и стикерпаки в ней:<blockquote expandable>{str(chest["stick"]).replace("{", "🟣").replace("], ", "],\n🟣").replace("}", "")}</blockquote>"""
        await message.reply(text, parse_mode="HTML")
        closechest(chest)
        







## Случайный стикер
async def rs(message: types.Message, args: str):
    chest = openchest()
    topic = random.choice(list(chest["stick"].keys()))
    pack = random.choice(chest["stick"][topic])
    try:
        sticker_set = await bot.get_sticker_set(name=pack)
    except Exception as e:
        return await message.reply(f"БЕЗ СПАМА БЕЗ СПАМА!!!!")
    allowed = [s for s in sticker_set.stickers if s.file_unique_id not in chest["badstick"]]
    if not allowed:
        return await message.reply("во те на те стикеры в квадрате все стикеры с матюками")
    sticker = random.choice(allowed)
    await message.answer_sticker(sticker.file_id)


### Рандом на "орлюк"
async def orluk(message: types.Message, args: str):
    query = "орел"
    tes = random.choice([rv, rp])
    eagle = await tes(message, query)
    if tes == rp:
        await message.answer_photo(eagle[1], caption=args)
    else:
        await message.answer_animation(eagle[1], caption=args)


### Случайные картинки/видео
## НЕ НЕЙРОНИТЬ ПЛИЗ
def noaipls(hits):
    bad_tokens = ("neural", "ai-art", "ai_generated", "generated", "aiart", "нейросеть",  "искусственный интеллект", "созданный ии", "ии генерируется", "ai сгенерирован", "сгенерированный ии", "и сгенерировано")
    filtered = []
    for h in hits:
        klu = []
        for key in ["tags", "page", "user", "alt", "image"]:
            keyk = h.get(key)
            if not isinstance(keyk, str):
                continue
            klu.append(keyk)
        if any(bt in str(klu).lower() for bt in bad_tokens):
            continue
        filtered.append(h)
    return filtered
## ДЛЯ ПЕКСЕЛЯ
def thingforpexel(quer, query, color):
    texting = quer.split()
    maxpage = 80
    if len(texting) > 0 and texting[0].startswith("-") and texting[0].lstrip("-").isdigit():
        if int(texting[0].lstrip("-")) == 0:
            page = 1
        elif int(texting[0].lstrip("-")) < maxpage:
            page = int(texting[0].lstrip("-"))
        else:
            page = maxpage
    else:
        page = maxpage
    if bool(re.search(r'[\u0400-\u04FF]', query)):
        lang = "ru-RU"
    else:
        lang = "en-US"
    key = {"Authorization": PEXELS_KEY}
    params = {"query": query, "per_page": page, "locale": lang, "color": color}
    return key, params
## Фильтр поиска + Пиксебей
def queryfilter(message, query, com):
    if message.reply_to_message:
        query = message.reply_to_message.text or query
    if not query:
        query = random.choice(DEFAULT_QUERY)
    if message.text:
        R = message.text.startswith(f"/{com}")
    else:
        R = ""
    texting = query.split()
    n = 0
    maxpage = 200
    page = maxpage
    lang = "ru"
    quer = ""
    color = ""
    pexel = False
    while n < len(texting):
        if texting[n].startswith("-"):
            if texting[n].lstrip("-").isdigit():
                if int(texting[n].lstrip("-")) < 3:
                    page = 3
                elif int(texting[n].lstrip("-")) < maxpage:
                    page = int(texting[n].lstrip("-"))
                else:
                    page = maxpage
            elif texting[n].startswith("-color:") and texting[n].lstrip("-color:") in colorit:
                color = texting[n].lstrip("-color:")
            elif texting[n].startswith("-lang:") and texting[n].lstrip("-lang:") in langa:
                lang = texting[n].lstrip("-lang:")
            elif texting[n].startswith("-pexel"):
                pexel = True
            n += 1
        else:
            while n < len(texting):
                quer += f"{texting[n]} "
                n += 1
            break
    query = quer.strip()
    if not query:
        query = random.choice(DEFAULT_QUERY)
    return R, query, page, color, lang, pexel
## Генератор случайных картинок
async def rp(message: types.Message, quer: str):
    query = quer
    RP, query, page, color, lang, pexel = queryfilter(message, query, "rp")
    params = {"key": PIXABAY_KEY, "q": query, "image_type": "all", "safesearch": "true", "per_page": page, "colors": color, "lang": lang, "order": "latest"}
    try:
        if not pexel:
            resp = requests.get("https://pixabay.com/api/", params=params, timeout=5)
            data = resp.json()
            hits = data.get("hits", [])
        else:
            hits = False
    except Exception as e:
        hits = False
        pass
    if not hits:
        key, params = thingforpexel(quer, query, color)
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
    RV, query, page, color, lang, pexel = queryfilter(message, query, "rv")
    params = {"key": PIXABAY_KEY, "q": query, "video_type": "all", "per_page": page, "lang": lang, "order": "latest"}
    try:
        if not pexel:
            resp = requests.get("https://pixabay.com/api/videos/", params=params, timeout=5)
            data = resp.json()
            hits = data.get("hits", [])
        else:
            hits = False
    except Exception:
        hits = False
        pass
    if not hits:
        key, params = thingforpexel(quer, query, "")
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
    url = video_data.get("tiny", {}).get("url", "") or choice["video_files"][0]["link"]
    if url:
        video_url = url.replace("http://", "https://")
        if RV:
            return await message.answer_animation(video_url)
        else:
            return query, video_url


### ТЕКСТ НА КАРТИНКУ
async def ttm(message: types.Message, args: str):
    return await message.reply("команда не работает ибо Бармен страдает от запросов Липсела. Извините")
    rep = message.reply_to_message or message
    media = rep.photo[-1] if rep.photo else rep.animation or rep.sticker or rep.video
    args = (args if len(args) > 0 else message.reply_to_message.text or args) if message.reply_to_message else args
    isvideo = False
    x = 0
    y = 0
    texting = args.split()
    if media and not (rep.sticker and rep.sticker.is_animated):
        x = media.width
        y = media.height
        pic = await bot.get_file(media.file_id)
        if rep.photo:
            forma = "png"
        elif rep.sticker and rep.sticker.is_video:
            forma = "webm"
        elif rep.sticker:
            forma = "webp"
        elif rep.animation or rep.video:
            forma = "mp4"
            isvideo = True
        infile = f"/tmp/in.{forma}"
        picpic = await bot.download_file(pic.file_path, infile)
    else:
        if len(texting) > 0 and texting[0] == "-v":
            forma = "mp4"
            isvideo = True
        else:
            forma = "png"
            isvideo = False
    by = picpic.read()
    await message.answer("T1")
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field(
            "file",
            by,
            filename=f"in.{forma}",
            content_type=f"in/{forma}"
        )
        data.add_field("args", args)
        data.add_field("type", forma)
        data.add_field("isvideo", isvideo)
        data.add_field("x", x)
        data.add_field("y", y)
        async with session.post(
            URL_TWO + "process",
            data=data
        ) as resp:
            proc, result = await resp.read()
    if not proc:
        await message.answer(f"T2: {result}")
        return await message.answer(result)
    await message.answer(f"T3: {proc}")
    outfile = f"/tmp/out.{type}"
    formo = False
    if forma == "webm" and not texting[0] == "-v":
        forma = "webp"
        formo = True
    elif forma == "webm" and texting[0] == "-v":
        forma = "mp4"
    try:
        if forma in ["webm", "webp"]:
            await message.answer_sticker(BufferedInputFile(result, outfile))
        if forma == "mp4":
            await message.answer_animation(BufferedInputFile(result, outfile))
        if forma == "png":
            await message.answer_photo(BufferedInputFile(result, outfile))
    except Exception as e:
        if str(e) == "Telegram server says - Bad Request: file must be non-empty":
            await message.answer(f"Я не всегда могу наносить текст на текст, надо другой стикер :/")
        else:
            await message.answer(f"Probla: {e}")
    os.remove(infile)
    os.remove(outfile)
    if formo:
        os.remove(f"/tmp/out.webm")


async def makaka(message: types.Message, args: str):
    chest = openchest()
    parts = (args or "").split()
    text = ""
    if len(parts) >= 2:
        bar = parts[0]
        if parts[1].lstrip("-").isdigit():
            men = int(parts[1])
        else:
            return await message.answer("Нужна ЦИФРА")
        if len(parts) >= 3:
            sho = parts[2]
        if bar == "-t" and parts[1].isdigit():
            text = "Время таймаута гифки/стикера"
            chest["timtim"]["timeout"] = men
        elif bar == "-m" and parts[1].isdigit():
            text = "Максимальный лимит гифок/стикеров за таймаут"
            chest["timtim"]["maxgif"] = men
        elif bar == "-tt" and parts[1].isdigit():
            text = 'Количество "тим" при отправке гифки/стикера'
            chest["timtim"]["timtext"] = men
        elif bar == "-v":
            if not len(parts) >= 3:
                return await message.answer("Пожалуйста, укажите айди гифки. Если вы не Бармен, спросите у него")
            if sho == "-all":
                text = 'Количество отправленных ВСЕХ гифок/стикеров, отправленные за последнее время'
                for key in chest["timtim"]["timrep"]:
                    if chest["timtim"]["timrep"][key]["VALUE"] > 0:
                        chest["timtim"]["timrep"][key]["VALUE"] = men
            else:
                for key in chest["timtim"]["timrep"]:
                    if sho == key:
                        text = f'Количество отправленной гифки/стикера "{chest["timtim"]["timrep"][key]["NAME"]}"'
                        chest["timtim"]["timrep"][key]["VALUE"] = men
                        break
                if not text:
                    return await message.answer("Пожалуйста, укажите правильное айди гифки. Если вы не Бармен, спросите у него")
        else:
            return await message.answer("Неверно указано ;(")
        if message.from_user.id == TIM_ID:
            return await message.reply("Неа.")
    else:
        texti = []
        for key in chest["timtim"]["timrep"]:
            text = f"""{chest["timtim"]["timrep"][key]["NAME"]}
📚Использовано за последнее время: {chest["timtim"]["timrep"][key]["VALUE"]} ед.
➡️До следующего понижения: {chest["timtim"]["timrep"][key]["TIME"]} м.
"""
            texti.append(text)
        jojo = "<blockquote expandable>" + ("".join(texti).strip() or "Гифок нету стикеров нету ;(") + "</blockquote>"
        return await message.answer(f"""
Параметры такие:
Таймаут гифок/стикеров [-t]: {chest["timtim"]["timeout"]} м.
Максимальный лимит гифок/стикеров за таймаут [-m]: {chest["timtim"]["maxgif"]} ед.
Количество "тим" [-tt]: {chest["timtim"]["timtext"]} ед.
Гифки/стикеры в целом [-v]:
{jojo}
""", parse_mode="HTML")
    await message.answer(f"Изменено:\n{text}: {men}")
    closechest(chest)


async def hmer(message: types.Message, args: str):
    chat_id = message.chat.id
    if chat_id != COVINOC_ID:
        return
    if message.from_user.id not in [PEKO_ID, ISCRA_ID, HURM_ID]:
        return await message.reply("Слишком опасно доверять эту кнопку всем. Обратитесь к Бармену.")
    try:
        await bot.unban_chat_member(chat_id, HURM_ID)
        return await message.reply(f"Хурма теперь есть.")
    except Exception as e:
        return await message.answer(f"Рошибка: {e}")


async def hkazn(message: types.Message, args: str):
    chat_id = message.chat.id
    if chat_id != COVINOC_ID:
        return
    if message.from_user.id not in [PEKO_ID, ISCRA_ID, HURM_ID]:
        return await message.reply("Слишком опасно доверять эту кнопку всем. Обратитесь к Бармену.")
    try:
        await bot.ban_chat_member(chat_id, HURM_ID)
        return await message.reply(f"Хурмы больше нету.")
    except Exception as e:
        return await message.answer(f"Рошибка: {e}")



### КНИИИИИИИИИИГА
async def guide(message: types.Message, args: str):
    await message.reply(f"""
КНИЖКА (Book📗📘) для использования бота:
🟪 - может работать с ответом на сообщение
❌ - команда не работает/временно не работает
<code>/start</code> - Проверка работы бота и когда запущен
<code>/guide</code> - КНИЖКА (Book📗📘) для использования бота
<code>/admin</code> - С шансом 1 к 2763 возможно выдаст админку
<code>/gm</code> - Желает доброго утра
<code>/id</code> - Выдаёт айди и уникальный айди медиа. Работает лишь в ЛС
<code>/like 'emoji'</code> - 🟪 Поставить реакцию сообщению ботом<blockquote expandable>    'emoji' - Эмоция, которая поддерживается в стандартном наборе реакций Telegram. Без параметра по умолчанию выдаёт 👍</blockquote>
<code>/nolike</code> - 🟪 Отобрать реакцию бота с ответа на сообщение
<code>/mathi 'diff'</code> - Решить задачку по математике за 10 секунд<blockquote expandable>    'diff' - сложность задачки. По умолчанию - easy:
    easy - Лёгкая сложность. Два числа от 1 до 100, между ними знак "плюс" либо "минус"
    medium - Средняя сложность. К каждому числу лёгкого режима добавляется число при знаке "умножить" либо "разделить" от 1 до 10
    hard - Сложная сложность. Три числа от 1 до 100, между ними знак "умножить" либо "разделить"</blockquote>
<code>/wts</code> - Выдать список доступных команд рандомных стикеров
<code>/rs</code> - Случайный стикер из списка <code>/wts</code>
<code>/orluk</code> - Случайное видео/фото орла
<code>/rp 'params' 'quote'</code> - 🟪 Поиск случайных фото по запросу
<code>/rv 'params' 'quote'</code> - 🟪 Поиск случайных видео по запросу<blockquote expandable>    По умолчанию поиск проводится по Pixabay, если не находит - ищет через Pexel.
    'params' - Параметры поиска:
    -pexel - Поиск через Pexel без Pixabay
    -n - Вместо n число от 1 до 200. Задаёт количество медиа, которые будут осмотрены. Для Pixabay значение от 3 до 200, для Pexel - от 1 до 80. По умолчанию - 200
    -lang: - Выбор языка из перечисленных ниже:
["cs", "da", "de", "en", "es", "fr", "id", "it", "hu", "nl", "no", "pl", "pt", "ro", "sk", "fi", "sv", "tr", "vi", "th", "bg", "ru", "el", "ja", "ko", "zh"]
    По умолчанию выставлено RU.
    -color: - Выбор приоритетного цвета из перечисленных ниже:
["grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown", "violet"]
    По умолчанию выставлены все цвета.
    'quote' - Запрос:
    По умолчанию выбирается запрос из текста ответа на сообщение. Если сообщение без текста - выбирается запрос из сообщения с командой. По умолчанию - Пиво</blockquote>
<code>/ttm 'format' 'quote'</code> - 🟪 ❌ Нанесение текста на нижнюю часть медиа<blockquote expandable>    Для команды требуется медиа в виде ответа либо в виде сообщения с описанием, в ином случае медиа будет подобрано из <code>/rp</code> либо <code>/rv</code>. 
    'format' - если выставлено -v, видео-стикеры будут отображаться в виде GIF, а подбор медиа будет осуществлено с помощью <code>/rv</code>. Если формат отсутсвует, видео-стикеры будут отображать лишь первый кадр, а подбор медиа будет осуществлено с помощью <code>/rp</code>.
    'quote' - текст, который будет нанесён на медиа. Эмоции будут отображены как невидимые символы. При отправке запроса на <code>/rp</code> или <code>/rv</code>, параметры для них учитываются.</blockquote>
""", parse_mode="HTML")























#### КОНСОЛЬНАЯ ХЕРНЯ
### Достать датабазу
async def data(message: types.Message, args: str):
    if message.from_user.id != PEKO_ID:
        return
    chest = openchest()
    text = json.dumps(chest, indent=4, ensure_ascii=False)
    if args == "B":
        text = text.replace("true", "True").replace("false", "False")
    file = BufferedInputFile(
        text.encode("utf-8"),
        filename="chest.json"
    )
    await message.answer_document(file)

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
### ЗАПИСЬ ЧАТА В ДЖСОН
    if f"{chat_id}" not in chest["rich"]:
        chest["rich"][f"{chat_id}"] = {
            "lab": False,
            "cmh": False,
            "cmt": False
        }
        closechest(chest)

    if message.left_chat_member and message.left_chat_member.id == HURM_ID:
        try:
            await bot.ban_chat_member(chat_id, user_id)
            await message.answer(f"Эх блин, Хурма ливнула! Очень жаль, что он не сможет вернуться ;(")
        except Exception as e:
            await message.answer(f"Рошибка: {e}")
        await bot.send_message(PEKO_ID, "ХУРМО ЛИВНУЛО")
### Мгновенная реакция
    if message.from_user.id == TIM_ID and chest["rich"][f"{chat_id}"]["cmt"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.from_user.id == HURM_ID and chest["rich"][f"{chat_id}"]["cmh"]:
        return await bot.delete_message(chat_id=chat_id, message_id=message.message_id)




### РАБОТА КОМАНД
    if (message.text and message.text.startswith("/")) or (message.caption and message.caption.startswith("/")):
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
            args = parts[1] if len(parts) > 1 else ""
            if cmd in chest["stick"]:
                pack_list = chest["stick"].get(cmd, [])
                if not pack_list:
                    return await message.reply("Бармен не предоставил мне стикерпаков =/")
                chosen = random.choice(pack_list)
                sticker_set = await bot.get_sticker_set(name=chosen)
                allowed = [s for s in sticker_set.stickers if s.file_unique_id not in chest["badstick"]]
                if not allowed:
                    return await message.reply("вот те на те все стикеры с матюками")
                sticker = random.choice(allowed)
                await message.answer_sticker(sticker.file_id)
            if cmd in chest["rich"][f"{chat_id}"]:
                await richagi(message, args, cmd)
            if cmd in comasiv:
                func = globals().get(cmd)
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
        media = message.photo[-1] if message.photo else message.animation or message.sticker or message.video or message.voice or message.document
        if media:
            file_id = media.file_id
            unique_id = media.file_unique_id
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
        if message.from_user.id == TIM_ID and (any(word.lower().startswith(mat) for word in message.text.split() for mat in MATUUUK) or any(matu in message.text.lower() for matu in FUL_MATUUUK)):
            await orluk(message, "")
        if "майнера крафтов" in message.text.lower():
            await message.reply("не зли меня, бяка >=(")

        if message.reply_to_message and message.text == "+" and message.reply_to_message.from_user.id == HURM_ID and message.chat.id == COVINOC_ID:
            if message.from_user.id == HURM_ID:
                await message.answer(f"Нет, ты не можешь сам себе балл сменить, лопух :Р")
            elif chest["hurma"]["hurmcd"]:
                await message.answer(f"КД на смену баллов Хурме, звиняйте, подождите немножечко :Ж")
            elif not chest["hurma"]["hurmcd"]:
                chest["hurma"]["hurmball"] += 1
                await message.answer(f"Хурме начислен балл! Текущее кол-во баллов Хурмы: {chest["hurma"]["hurmball"]}")
                chest["hurma"]["hurmcd"] = True

        if message.reply_to_message and message.text == "-" and message.reply_to_message.from_user.id == HURM_ID and message.chat.id == COVINOC_ID:
            if message.from_user.id == HURM_ID:
                await message.answer(f"Нет, ты не можешь сам себе балл сменить, лопух :Р")
            elif chest["hurma"]["hurmcd"]:
                await message.answer(f"КД на смену баллов Хурме, звиняйте, подождите немножечко :Ж")
            elif not chest["hurma"]["hurmcd"]:
                chest["hurma"]["hurmball"] -= 1
                await message.answer(f"Хурме отчислен балл! Текущее кол-во баллов Хурмы: {chest["hurma"]["hurmball"]}")
                chest["hurma"]["hurmcd"] = True

        if message.text.lower() == "баллы хурмы" and message.chat.id == COVINOC_ID:
            await message.answer(f"Текущее кол-во баллов Хурмы: {chest["hurma"]["hurmball"]}")
        if message.text.lower() == "мои баллы" and message.chat.id == COVINOC_ID and message.from_user.id == HURM_ID:
            await message.answer(f"Текущее ваше кол-во баллов: {chest["hurma"]["hurmball"]}")

    if message.animation or message.sticker:
        if message.from_user.id == TIM_ID:
            chest["timtim"]["timtext"] += 1
            if chest["timtim"]["timtext"] > 400:
                await message.answer(f"🎉🎊ов настолько много, что они не вмещаются в один текст, поэтому скажу число: {chest["timtim"]["timtext"]}")
            else:
                await message.answer("🎉🎊 " * chest["timtim"]["timtext"])
            if message.animation:
                unique_id = message.animation.file_unique_id
                id = message.animation.file_id
                name = message.animation.file_name or "GIF"
            if message.sticker:
                unique_id = message.sticker.file_unique_id
                id = message.sticker.file_id
                name = "Sticker " + message.sticker.emoji
            if message.photo:
                unique_id = message.photo[-1].file_unique_id
                id = message.photo[-1].file_id
                name = "Photo"
            if f"{unique_id}" not in chest["timtim"]["timrep"]:
                chest["timtim"]["timrep"][f"{unique_id}"] = {}
                chest["timtim"]["timrep"][f"{unique_id}"]["VALUE"] = 0
            chest["timtim"]["timrep"][f"{unique_id}"]["ID"] = id
            chest["timtim"]["timrep"][f"{unique_id}"]["NAME"] = name
            chest["timtim"]["timrep"][f"{unique_id}"]["TIME"] = chest["timtim"]["timeout"]
            chest["timtim"]["timrep"][f"{unique_id}"]["VALUE"] += 1
            if chest["timtim"]["timrep"][f"{unique_id}"]["VALUE"] > chest["timtim"]["maxgif"]:
                await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if message.photo and message.from_user.id == TIM_ID:
        try:
            buffer = BytesIO()
            aku = await bot.get_file(message.photo[-1].file_id)
            await bot.download_file(aku.file_path, buffer)
            buffer.seek(0)
            response = requests.post(
                "https://api.ocr.space/parse/image",
                files={"file": ("image.png", buffer, "image/png")},
                data={"apikey": "helloworld", "language": "rus", "OCREngine": 2}
            )
            result = response.json()
            testube = result["ParsedResults"][0]["ParsedText"].lower()
            areyousure = testube.replace(" ", "")
            print(testube or "No text ;(")
            if any(word.lower().startswith(mat) for word in testube.split() for mat in MATUUUK) or any(matu in areyousure for matu in FUL_MATUUUK):
                await orluk(message, "ты не думай, что я не вижу матюки в картинках, тим")
        except Exception as e:
            pass
    closechest(chest)



















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
        for i in range(60):
            await asyncio.sleep(60)
            chest = openchest()
            chest["hurma"]["hurmcd"] = False
            for key in chest["timtim"]["timrep"]:
                if chest["timtim"]["timrep"][key]["TIME"] > 0:
                    chest["timtim"]["timrep"][key]["TIME"] -= 1
                if chest["timtim"]["timrep"][key]["TIME"] == 0:
                    if chest["timtim"]["timrep"][key]["VALUE"] > 0:
                        chest["timtim"]["timrep"][key]["VALUE"] -= 1
                    chest["timtim"]["timrep"][key]["TIME"] = chest["timtim"]["timeout"]
            chest["timtim"]["timrep"] = {k: v for k, v in chest["timtim"]["timrep"].items() if not v["VALUE"] == 0}
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