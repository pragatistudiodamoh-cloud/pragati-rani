import os, asyncio, ctypes, glob, random, json, re, webbrowser, urllib.parse, time, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageGrab
from datetime import datetime

# ============ GITHUB - MADAN JI KA LINK - BILKUL SAHI ============
GITHUB_LINK = "https://raw.githubusercontent.com/pragatistudiodamoh-cloud/pragati-rani/main/agent.py"
VERSION_FILE = "rani_version.txt"

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
    if len(text) > 400: text = text[:400]
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

# ============ GITHUB SE UPDATE ============
async def github_se_update():
    import urllib.request, shutil
    try:
        print(f"[Rani - GitHub]: {GITHUB_LINK} se naya code la rahi hun...")
        req = urllib.request.Request(GITHUB_LINK, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            naya_code = r.read().decode('utf-8')
        if len(naya_code) < 1000:
            return "Madan ji, GitHub se code khaali aaya hai. Aapne agent.py GitHub pe dala hai na? Pehle upload karo."
        if os.path.exists("agent.py"):
            shutil.copy("agent.py", "agent_purana.py")
        open("agent.py", "w", encoding="utf-8").write(naya_code)
        v = 1
        if os.path.exists(VERSION_FILE):
            try: v = int(open(VERSION_FILE).read().strip()) + 1
            except: v = 1
        open(VERSION_FILE, "w").write(str(v))
        return f"Madan ji, ho gaya! Main GitHub se update ho gayi hun. Ab main Version {v} pe hun. Mujhe band karke fir se chalao - py agent.py"
    except Exception as e:
        return f"Madan ji, GitHub se update nahi ho payi. Pehle check karo ki agent.py GitHub pe dala hai ya nahi. Galti - {e}"

def abhi_time():
    abhi = datetime.now()
    ghanta = abhi.hour; minute = abhi.minute
    if ghanta < 12: waqt = "subah"
    elif ghanta < 16: waqt = "dopahar"
    elif ghanta < 19: waqt = "shaam"
    else: waqt = "raat"
    din_hindi = ["Somvaar", "Mangalvaar", "Budhvaar", "Guruvaar", "Shukravaar", "Shanivaar", "Ravivaar"]
    din = din_hindi[abhi.weekday()]
    ghanta12 = ghanta % 12
    if ghanta12 == 0: ghanta12 = 12
    return {"ghanta": ghanta, "minute": minute, "waqt": waqt, "din": din, "time_str": f"{ghanta12}:{minute:02d}", "poora": f"{din}, {waqt} ke {ghanta12}:{minute:02d} baj rahe hain", "date": abhi.day}

def samajhdar_greeting(order_raw):
    o = order_raw.lower().strip()
    t = abhi_time(); ghanta = t["ghanta"]
    if "good morning" in o:
        if ghanta >= 12 and ghanta < 16: return f"Are Madan ji, Good Morning nahi, abhi to dopahar hai! Abhi {t['time_str']} baj rahe hain, Good Afternoon bolo!"
        elif ghanta >= 16: return f"Madan ji, abhi to shaam ho gayi hai, {t['time_str']} baj rahe hain. Good Evening bolo!"
        else: return f"Good Morning Madan ji! Subah ke {t['time_str']} baj rahe hain. Chai pi li?"
    if "good afternoon" in o:
        if ghanta < 12: return f"Madan ji, abhi to subah hai, {t['time_str']} baj rahe hain. Abhi Good Morning bolo."
        elif ghanta >= 16: return f"Madan ji, abhi to shaam ho gayi hai, {t['time_str']} baj rahe hain. Ab Good Evening bolo."
        else: return f"Good Afternoon Madan ji! Dopahar ke {t['time_str']} baj rahe hain. Khana kha liya?"
    if "good evening" in o:
        if ghanta < 16: return f"Madan ji, abhi to {t['waqt']} hai, {t['time_str']} baj rahe hain."
        else: return f"Good Evening Madan ji! Shaam ke {t['time_str']} baj rahe hain."
    if "good night" in o:
        if ghanta < 19 and ghanta >= 5: return f"Madan ji, abhi to {t['waqt']} hai, {t['time_str']} baj rahe hain. Good Night to raat ko bolte hain."
        else: return f"Good Night Madan ji! Raat ke {t['time_str']} baj rahe hain."
    if "namaste" in o or "hello" in o or o in ["hi", "hey"]:
        return f"Namaste Madan ji! {t['poora']}. Bolo kya kaam hai?"
    if "kaise ho" in o or "kya haal" in o: return f"Main bilkul badhiya hun Madan ji. Abhi {t['poora']}."
    if "kitne baje" in o or "time" in o: return f"Madan ji, abhi {t['poora']}."
    if "kaunsa din" in o or "kaun sa din" in o or "date" in o: return f"Madan ji, aaj {t['din']} hai, {t['date']} tarikh hai."
    return None

async def naya_seekho(sawaal):
    import urllib.request, json as js
    try:
        prompt = f"Tum Rani ho, Madan ji ki FULL AI Assistant. Simple Hindi me, gaon ki bhasha me, 2-3 line me samjhao. Sawaal: {sawaal}"
        data = js.dumps({"messages": [{"role": "user", "content": prompt}], "model": "openai"}).encode()
        req = urllib.request.Request("https://text.pollinations.ai/openai", data=data, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            res = js.loads(r.read())
            j = res["choices"][0]["message"]["content"].strip()
            if j: return saaf_karo(j)
    except: pass
    return "Madan ji, iske baare me main internet se naya seekh ke batati hun."

def software_dhoondho(naam):
    khoj_jagah = [r"C:\Program Files", r"C:\Program Files (x86)"]
    khoj_naam = {"photoshop": ["Photoshop.exe"], "album": ["Album Xpress.exe", "AlbumXpress.exe", "AX.exe", "Album.exe"]}
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
        subprocess.Popen([rasta]); time.sleep(4); return True
    try:
        if naam == "photoshop": os.system('start "" "Photoshop"')
        elif naam == "album": os.system('start "" "Album Xpress"')
        time.sleep(4); return True
    except: pass
    return False

async def photoshop_kaam(order):
    await rani_boli("Thik hai Madan ji, main asli Photoshop khol rahi hun.")
    if not software_kholo("photoshop"):
        await rani_boli("Madan ji, Photoshop is PC me mila nahi.")
        return
    await rani_boli("Ho gaya Madan ji, Photoshop khul gaya hai. Bolo kya karna hai - Card banana hai ya Photo gora karna hai?")

async def album_kaam(order):
    await rani_boli("Thik hai Madan ji, main Album Xpress khol rahi hun.")
    if not software_kholo("album"):
        await rani_boli("Madan ji, Album Xpress is PC me nahi mila. Desktop pe uska icon dikhao.")
        return
    await rani_boli("Ho gaya Madan ji, Album Xpress khul gaya hai. Naya album bana rahi hun.")
    if HAS_PY:
        await asyncio.sleep(2); pyautogui.hotkey('ctrl', 'n'); await asyncio.sleep(1)
    await rani_boli("Madan ji, naya album wala dabba khol diya hai.")

def samajh_pehchano(order_raw):
    o = order_raw.lower().strip()
    if "github" in o and ("update" in o or "naya" in o): return "GITHUB_UPDATE"
    if "version" in o or "kaunsa version" in o: return "VERSION_BATAO"
    if any(w in o for w in ["good morning", "good afternoon", "good evening", "good night", "namaste", "hello", "kaise ho", "kitne baje", "kaunsa din", "time"]): return "SAMAJHDAR"
    if "mausam" in o: return "MAUSAM"
    if "album" in o or "xpress" in o or "digiflick" in o: return "ALBUM"
    if "photoshop" in o: return "PHOTOSHOP"
    if "screen" in o and "dekh" in o: return "SCREEN"
    if "youtube" in o or "gaana" in o: return "YOUTUBE"
    if "whatsapp" in o: return "WHATSAPP"
    if "google" in o: return "GOOGLE"
    if o in ["ha", "haa", "haan", "ok"]: return "BAAT"
    if any(w in o for w in ["banao", "bana", "khol", "karo", "kar"]): return "KAAM"
    if any(w in o for w in ["kaise", "kaunsa", "kyun", "kya hai", "batao", "samjhao"]): return "SAWAAL"
    return "SAMAJH_NAHI"

async def main():
    t = abhi_time()
    if t["ghanta"] < 12: shuru = f"Good Morning Madan ji! Subah ke {t['time_str']} baj rahe hain. Main aapki FULL AI Assistant Rani hazir hun."
    elif t["ghanta"] < 16: shuru = f"Good Afternoon Madan ji! Dopahar ke {t['time_str']} baj rahe hain. Main Rani hazir hun."
    elif t["ghanta"] < 19: shuru = f"Good Evening Madan ji! Shaam ke {t['time_str']} baj rahe hain. Main Rani hazir hun."
    else: shuru = f"Namaste Madan ji! Raat ke {t['time_str']} baj rahe hain. Main Rani hazir hun."
    await rani_boli(shuru + " Ab main GitHub se bhi update ho sakti hun. Bolo - GitHub se update ho jao.")
    while True:
        order_raw = input("Aap: ")
        order = order_raw.lower().strip()
        if order in ["band", "bye", "ruk"]:
            await rani_boli("Thik hai Madan ji, main ja rahi hun."); break
        kism = samajh_pehchano(order_raw)
        print(f"[Rani ki samajh]: Ye {kism} hai - {order_raw}")
        if kism == "GITHUB_UPDATE":
            await rani_boli("Thik hai Madan ji, main GitHub se update ho rahi hun, pragatistudiodamoh-cloud wali almari se naya code la rahi hun.")
            jawab = await github_se_update()
            await rani_boli(jawab)
            continue
        if kism == "VERSION_BATAO":
            v = "1"
            if os.path.exists(VERSION_FILE):
                v = open(VERSION_FILE).read().strip()
            await rani_boli(f"Madan ji, main abhi Version {v} pe hun. GitHub se update karke naya version la sakti hun.")
            continue
        if kism == "SAMAJHDAR":
            jawab = samajhdar_greeting(order_raw)
            if jawab: await rani_boli(jawab)
            else: await rani_boli("Haan Madan ji, bolo.")
            continue
        if kism == "MAUSAM":
            await rani_boli(await naya_seekho("Damoh me aaj ka mausam kaisa hai")); continue
        if kism == "ALBUM": await album_kaam(order); continue
        if kism == "PHOTOSHOP": await photoshop_kaam(order); continue
        if kism == "SCREEN":
            await rani_boli("Thik hai Madan ji, main screen dekh rahi hun.")
            try: ImageGrab.grab().save("rani_screen.png"); await rani_boli("Madan ji, screen ka photo le liya hai, dekh liya hai.")
            except: await rani_boli("Madan ji, screen nahi dekh payi.")
            continue
        if kism == "YOUTUBE":
            khoj = order.replace("youtube", "").replace("gaana", "").replace("chalao", "").strip()
            if not khoj: khoj = "Arijit Singh songs"
            webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(khoj)}")
            await rani_boli(f"Ho gaya Madan ji, YouTube pe {khoj} chala diya hai.")
            continue
        if kism == "WHATSAPP":
            webbrowser.open("https://web.whatsapp.com"); await rani_boli("Ho gaya Madan ji, WhatsApp khol diya hai."); continue
        if kism == "GOOGLE":
            khoj = order.replace("google me", "").replace("google", "").strip()
            if not khoj: khoj = "Pragati Studio Damoh"
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(khoj)}"); await rani_boli(f"Ho gaya Madan ji, Google me {khoj} khol diya hai."); continue
        if kism == "BAAT":
            await rani_boli("Haan Madan ji, bolo."); continue
        if kism == "KAAM":
            await rani_boli("Madan ji, bolo Photoshop me karna hai ya Album Xpress me?"); continue
        if kism == "SAWAAL":
            await rani_boli(await naya_seekho(order_raw)); continue
        if kism == "SAMAJH_NAHI":
            await rani_boli("Madan ji, samajh nahi aaya. Bolo - GitHub se update ho jao ya Photoshop kholo ya Album Xpress kholo?")
            continue

asyncio.run(main())