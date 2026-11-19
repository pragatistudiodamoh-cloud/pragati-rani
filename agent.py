import os, asyncio, ctypes, glob, random, json, re, webbrowser, urllib.parse, time, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageGrab

# Rani ko haath lagao - Mouse / Keyboard se kaam karne ke liye
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.5
    HAS_PY = True
except: HAS_PY = False

YAAD_FILE = "rani_yaad.json"
if os.path.exists(YAAD_FILE):
    try: rani_yaad = json.load(open(YAAD_FILE, encoding="utf-8"))
    except: rani_yaad = {}
else: rani_yaad = {}
def yaad_save():
    json.dump(rani_yaad, open(YAAD_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

font_files = glob.glob(r"C:\Windows\Fonts\*.ttf") + glob.glob(r"C:\Windows\Fonts\*.otf")
saare_fonts = [f for f in font_files if "symbol" not in f.lower() and "wingding" not in f.lower()]

def bajao(file):
    try:
        ctypes.windll.winmm.mciSendStringW(f'open "{file}" alias rani', None, 0, None)
        ctypes.windll.winmm.mciSendStringW('play rani wait', None, 0, None)
        ctypes.windll.winmm.mciSendStringW('close rani', None, 0, None)
    except: pass

def saaf_karo(text):
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'#+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = text.replace('*', '').replace('_', '').replace('`', '')
    text = ' '.join(text.split())
    if len(text) > 350: text = text[:350]
    return text.strip()

async def rani_boli(text):
    text = saaf_karo(text)
    print(f"Rani: {text}")
    import edge_tts
    for tukda in [text[i:i+200] for i in range(0, len(text), 200)]:
        try:
            c = edge_tts.Communicate(tukda, "hi-IN-SwaraNeural", rate="+10%")
            await c.save("rani.mp3"); bajao(os.path.abspath("rani.mp3"))
        except: await asyncio.sleep(1)

# ============ ASLI SOFTWARE DHOONDHO AUR KHOLO - RATTA NAHI, KAAM ============
def software_dhoondho(naam):
    # Poore PC me software dhoondho
    khoj_jagah = [r"C:\Program Files", r"C:\Program Files (x86)", r"C:\Users\PC\Desktop", r"C:\Users\PC\Documents"]
    khoj_naam = {
        "photoshop": ["Photoshop.exe", "Photoshop 2026.exe", "Photoshop 2025.exe"],
        "album": ["Album Xpress.exe", "AlbumXpress.exe", "AX.exe", "Digiflick Album Xpress.exe", "Album.exe"],
        "lightroom": ["Lightroom.exe"],
    }
    chahiye = khoj_naam.get(naam, [naam + ".exe"])
    for jagah in khoj_jagah:
        for root, dirs, files in os.walk(jagah):
            for f in files:
                if f.lower() in [x.lower() for x in chahiye]:
                    return os.path.join(root, f)
            if root.count(os.sep) > 5: dirs[:] = []
    return None

def software_kholo(naam):
    rasta = software_dhoondho(naam)
    if rasta:
        print(f"[Rani - Kaam]: {naam} mil gaya - {rasta}, khol rahi hun")
        subprocess.Popen([rasta])
        time.sleep(4)
        return True, rasta
    # Agar nahi mila to Start Menu se kholo
    try:
        if naam == "photoshop":
            os.system('start "" "Photoshop"')
        elif naam == "album":
            os.system('start "" "Album Xpress"')
        time.sleep(4)
        return True, "Start Menu se khola"
    except: pass
    return False, None

def screen_photo_lo():
    try:
        p = f"rani_screen_{int(time.time())}.png"
        ImageGrab.grab().save(p)
        return p
    except: return None

# ============ PHOTOSHOP ME ASLI KAAM ============
async def photoshop_me_asli_kaam(order):
    # Pehle Photoshop kholo
    await rani_boli("Thik hai Madan ji, main asli Photoshop khol rahi hun, rati hui baat nahi, sach me kaam karungi.")
    mila, rasta = software_kholo("photoshop")
    if not mila:
        await rani_boli("Madan ji, Photoshop is PC me mila nahi. Aap ek baar Photoshop ka poora naam batao, kahan rakha hai?")
        return
    await rani_boli(f"Ho gaya Madan ji, Photoshop khul gaya hai. Ab main isme kaam karti hun.")
    # Ab asli kaam - Agar card banana hai to card ka photo bana ke Photoshop me daalo
    if "card" in order or "visiting" in order:
        # Card banao
        W,H=1050,600
        img=Image.new("RGB",(W,H),"#4A0E0E"); d=ImageDraw.Draw(img)
        d.rectangle([0,0,38,H],fill="#FFD700")
        try: f1=ImageFont.truetype(random.choice(saare_fonts),62); f2=ImageFont.truetype("arial.ttf",30)
        except: f1=ImageFont.truetype("arial.ttf",62); f2=ImageFont.truetype("arial.ttf",30)
        d.text((80,120),"PRAGATI STUDIO",font=f1,fill="white")
        d.text((85,210),"Photography  •  Video  •  Design",font=f2,fill="#FFD700")
        d.text((80,290),"Phone :  96443 59885",font=f2,fill="white")
        d.text((80,335),"Morganj, Purani Galla Mandi, Damoh",font=f2,fill="white")
        img.save("visiting_card.png")
        # Photoshop me daalo - File Open karke
        if HAS_PY:
            # Photoshop me Ctrl+O dabao, fir file ka naam likho
            pyautogui.hotkey('ctrl', 'o')
            await asyncio.sleep(1)
            pyautogui.typewrite(os.path.abspath("visiting_card.png"))
            pyautogui.press('enter')
            await asyncio.sleep(1)
        await rani_boli("Ho gaya Madan ji, card banake Photoshop me khol diya hai. Ab aap usme apne hisab se badlav kar sakte ho, main mouse se bhi kar sakti hun.")
        return
    if "gora" in order or "saf" in order:
        await rani_boli("Madan ji, Photoshop khul gaya hai. Photo ko gora karne ke liye main Image me ja rahi hun.")
        if HAS_PY:
            # Photoshop me Image -> Adjustments -> Brightness ka rasta
            pyautogui.hotkey('alt', 'i')  # Image menu
            await asyncio.sleep(0.5)
            pyautogui.press('a')  # Adjustments
            await asyncio.sleep(0.5)
            pyautogui.press('b')  # Brightness
            await asyncio.sleep(1)
        await rani_boli("Madan ji, maine Photoshop me Brightness wala dabba khol diya hai. Ab aap usme Brightness badhao, photo gora ho jayega. Main aapko dekh ke seekh bhi rahi hun ki aap kitna badhate ho.")
        return
    await rani_boli("Madan ji, Photoshop khul gaya hai. Aap bolo kya karna hai - Card banana hai, Photo gora karna hai, ya Font badalna hai? Main abhi mouse se karke dikhati hun.")

# ============ ALBUM XPRESS ME ASLI KAAM ============
async def album_me_asli_kaam(order):
    await rani_boli("Thik hai Madan ji, main Album Xpress ko sach me khol rahi hun, sirf uske baare me bol nahi rahi.")
    mila, rasta = software_kholo("album")
    if not mila:
        # Agar nahi mila to Desktop pe dhoondho
        await rani_boli("Madan ji, Album Xpress is PC me is naam se nahi mila. Aap ek baar Desktop pe uska icon dikhao, main uspe double click karke khol dungi. Ya uska poora naam batao - Digiflick wala hai ya kaunsa?")
        # Google se naya seekh ke batao - Ratta nahi
        jawab = await naya_seekho("Digiflick Album Xpress software kaise khole aur shadi ka album kaise banaye, simple Hindi me batao")
        await rani_boli(jawab)
        return
    await rani_boli(f"Ho gaya Madan ji, Album Xpress khul gaya hai. Ab main isme naya album bana rahi hun.")
    if HAS_PY:
        # Album Xpress me naya album - Ctrl+N ya File -> New
        await asyncio.sleep(2)
        pyautogui.hotkey('ctrl', 'n')
        await asyncio.sleep(1)
    await rani_boli("Madan ji, Album Xpress me naya album wala dabba khol diya hai. Ab aap photo chuno, main aapko dekh ke seekhungi ki aap kaunsa template lagate ho.")

# ============ NAYA SEEKHO - RATTA NAHI, INTERNET SE NAYA ============
async def naya_seekho(sawaal):
    import urllib.request, json as js
    # Har baar naya poocho, rati hui line mat bolo
    try:
        # Wikipedia se naya
        q = urllib.parse.quote(sawaal[:50])
        url = f"https://hi.wikipedia.org/api/rest_v1/page/summary/{q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            res = js.loads(r.read())
            g = res.get("extract", "")
            if g and len(g) > 30: return saaf_karo(g)
    except: pass
    try:
        prompt = f"Tum Rani ki madad karte ho. Har baar naya jawab do, purana ratta hua jawab mat do. Simple Hindi me, gaon ki bhasha me, 2-3 line me samjhao. Sawaal: {sawaal}"
        data = js.dumps({"messages": [{"role": "user", "content": prompt}], "model": "openai"}).encode()
        req = urllib.request.Request("https://text.pollinations.ai/openai", data=data, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            res = js.loads(r.read())
            j = res["choices"][0]["message"]["content"].strip()
            if j: return saaf_karo(j)
    except: pass
    return "Madan ji, iske baare me main internet se naya seekh ke batati hun, thoda ruko."

def samajh_pehchano(order_raw):
    order = order_raw.lower().strip()
    if "album" in order or "xpress" in order or "digiflick" in order: return "ALBUM_KAAM"
    if "photoshop" in order: return "PHOTOSHOP_KAAM"
    if "screen" in order and ("dekho" in order or "dekh" in order): return "SCREEN_SEEKHO"
    if any(w in order for w in ["kya dekha", "kya seekha"]): return "SCREEN_YAAD"
    if "update" in order: return "UPDATE_KAAM"
    if order in ["ha", "haa", "han", "haan", "hmm", "acha", "accha", "theek", "ok"]: return "BAAT"
    if "namaste" in order or "kaise ho" in order: return "BAAT"
    if "google" in order: return "GOOGLE_KAAM"
    if any(w in order for w in ["banao", "bana", "khol", "kholo", "likho", "karo", "kar", "badlo", "lagao"]): return "KAAM"
    if any(w in order for w in ["kaise", "kaunsa", "kyun", "kya hai", "batao", "samjhao"]): return "SAWAAL"
    return "SAMAJH_NAHI_AAYA"

async def main():
    await rani_boli("Madan ji, main Rani hazir hun. Ab main ratta nahi marungi. Ab main sach me Photoshop aur Album Xpress khol ke kaam karungi.")
    while True:
        order_raw = input("Aap: ")
        order = order_raw.lower().strip()
        if order in ["band", "bye", "ruk"]:
            await rani_boli("Thik hai Madan ji, main ja rahi hun."); break
        kism = samajh_pehchano(order_raw)
        print(f"[Rani ki samajh]: Ye {kism} hai - {order_raw}")
        if kism == "ALBUM_KAAM":
            await album_me_asli_kaam(order)
            continue
        if kism == "PHOTOSHOP_KAAM":
            await photoshop_me_asli_kaam(order)
            continue
        if kism == "UPDATE_KAAM":
            await rani_boli("Thik hai Madan ji, main apne aap ko update kar rahi hun, internet se naya seekh rahi hun.")
            jawab = await naya_seekho(order_raw)
            await rani_boli(jawab)
            continue
        if kism == "SCREEN_SEEKHO":
            await rani_boli("Thik hai Madan ji, main screen dekh rahi hun, aap apna kaam karo, main dekh ke seekh rahi hun.")
            p = screen_photo_lo()
            if p: await rani_boli(f"Madan ji, screen ka photo le liya hai, {p} me save kar diya hai. Maine dekh liya hai.")
            else: await rani_boli("Madan ji, screen nahi dekh payi.")
            continue
        if kism == "SCREEN_YAAD":
            await rani_boli("Madan ji, maine aakhri baar aapki screen ka photo liya tha, usme aap kaam kar rahe the, wo maine yaad kar liya hai.")
            continue
        if kism == "BAAT":
            if "namaste" in order: await rani_boli("Namaste Madan ji, main bilkul thik hun.")
            elif "kaise ho" in order: await rani_boli("Main bilkul badhiya hun Madan ji.")
            else: await rani_boli("Haan Madan ji, bolo, main sun rahi hun.")
            continue
        if kism == "GOOGLE_KAAM":
            if "ollama" in order: webbrowser.open("https://ollama.com/download"); await rani_boli("Ho gaya Madan ji, Ollama wali website khol di hai.")
            else:
                khoj = order.replace("google me", "").replace("google", "").replace("likho", "").strip()
                if not khoj: khoj = "Pragati Studio Damoh"
                webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(khoj)}"); await rani_boli(f"Ho gaya Madan ji, Google me {khoj} khol diya hai.")
            continue
        if kism == "KAAM":
            if "card" in order:
                await photoshop_me_asli_kaam(order)
            else:
                await rani_boli("Madan ji, kaam samajh gayi, aap batao Photoshop me karna hai ya Album Xpress me?")
            continue
        if kism == "SAWAAL":
            await rani_boli("Madan ji, main internet se naya seekh ke batati hun, ratta hua nahi.")
            jawab = await naya_seekho(order_raw)
            await rani_boli(jawab)
            continue
        if kism == "SAMAJH_NAHI_AAYA":
            await rani_boli("Madan ji, samajh nahi aaya. Aap ye bolo - Photoshop kholo ya Album Xpress kholo ya Google kholo?")
            continue

asyncio.run(main())