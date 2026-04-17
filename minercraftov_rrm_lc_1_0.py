#### ВЕРСИИ:
# 1.0 - релиз портативного rrm

#### ПЕРЕМЕННЫЕ БОТА
### БИБЛИОТЕКИ

import re, random, requests, json, ffmpeg, subprocess, math, aiohttp, os, base64
from PIL import ImageFont
from fastapi import FastAPI, UploadFile, Form
from dotenv import load_dotenv

load_dotenv()
PIXABAY_KEY = os.getenv("E_PIXABAY_KEY")
PEXELS_KEY = os.getenv("E_PEXELS_KEY")
DEFAULT_QUERY = json.loads(os.getenv("E_DEFAULT_QUERY", '""'))


app = FastAPI()

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
        print(str(klu).lower())
        filtered.append(h)
    return filtered

## Много, поэтому
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

colorit = ["grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown", "violet"]
langa = ["cs", "da", "de", "en", "es", "fr", "id", "it", "hu", "nl", "no", "pl", "pt", "ro", "sk", "fi", "sv", "tr", "vi", "th", "bg", "ru", "el", "ja", "ko", "zh"]
## Человек написал или кто
def queryfilter(message, query):
    if message.reply_to_message:
        query = message.reply_to_message.text or query
    if not query:
        query = random.choice(DEFAULT_QUERY)
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
    return query, page, color, lang, pexel

## Генератор случайных картинок
def rp(message: str, quer: str):
    query = quer
    query, page, color, lang, pexel = queryfilter(message, query)
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
        except Exception:
            return False, False
        if not hits:
            return False, False
    filtered = noaipls(hits)
    pool = filtered or hits
    choice = random.choice(pool)
    img_url = choice.get("webformatURL") or choice["src"]["large"]
    return query, img_url

## Генератор случайных видео
def rv(message: str, quer: str):
    query = quer
    query, page, color, lang, pexel = queryfilter(message, query)
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
        except Exception:
            return False, False
        if not hits:
            return False, False
    filtered = noaipls(hits)
    pool = filtered or hits
    choice = random.choice(pool)
    video_data = choice.get("videos", {})
    url = video_data.get("tiny", {}).get("url", "") or choice["video_files"][0]["link"]
    if url:
        video_url = url.replace("http://", "https://")
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







@app.post("/process")
async def process(pic: UploadFile, args: str = Form(), type: str = Form(), isvideo: str = Form(), x: str = Form(), y: str = Form()):
    isvideo = isvideo == "True"
    x = int(x)
    y = int(y)
    texting = args.split()
    args = args.removeprefix("-v").strip()
    if not args:
        args = random.choice(DEFAULT_QUERY)
    if not type:
        if len(texting) > 0 and texting[0] == "-v":
            ran = rv
            type = "mp4"
            isvideo = True
        else:
            ran = rp
            type = "png"
            isvideo = False
        infile = f"/tmp/in.{type}"
        outfile = f"/tmp/out.{type}"
        arga, htp = ran(message, args)
        if not arga:
            return {"ok": False, "error": "я ничо не нашла эх блин"}
        else:
            args = arga
        async with aiohttp.ClientSession() as session:
            async with session.get(htp) as resp:
                if resp.status != 200:
                    return {"ok": False, "error": "ничо не скачалось эх блин ;("}
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
    else:
        data = await pic.read()
        with open(infile, "wb") as f:
            f.write(data)
        infile = f"/tmp/in.{type}"
        outfile = f"/tmp/out.{type}"
    if type == "webm" and not texting[0] == "-v":
        type = "webp"
        ohno = subprocess.run(
            ["ffmpeg", "-i", infile, "-vframes", "1", f"/tmp/in.{type}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        infile = f"/tmp/in.{type}"
        outfile = f"/tmp/out.{type}"
    elif type == "webm" and texting[0] == "-v":
        type = "mp4"
        ohno = subprocess.run(
            ["ffmpeg", "-i", infile, f"/tmp/in.{type}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        infile = f"/tmp/in.{type}"
        outfile = f"/tmp/out.{type}"
    font = "Lobster.ttf"
    size = min(x, y)/10
    mlt = 80*(x/y)
    mwt = x*0.85
    mina = x/100
    outl = x/150
    textout, fontout, sizeout = textstab(x, y, args.lower(), mlt, mwt, size, font, mina)
    textout = textout.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
    comas = ["ffmpeg", "-y", "-i", infile, "-vf", f"fps=24,drawtext=fontfile={font}:text='{textout}':x=(w-text_w)/2:y=(h-text_h)/2+h*0.8/2:fontsize={sizeout}:fontcolor=white:borderw='{outl}':bordercolor=black"]
    if isvideo:
        comas += ["-c:v", "libx264", "-preset", "veryfast", "-threads", "2", "-an"]
    comas += [outfile]
    ohno = subprocess.run(
        comas,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    with open(output, "rb") as f:
        outo = f.read()
    return {
        "ok": True,
        "error": "",
        "file": base64.b64encode(outo).decode()
    }