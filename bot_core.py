# ═══════════════════════════════════════════════════════════════
# bot_core.py — YASIN × BHAI SUPER BOT (Full Combined & Refreshed)
# © 2025 YASIN × BHAI — All rights reserved
# ═══════════════════════════════════════════════════════════════

import sys, asyncio, random, json, os, time, math, pickle, traceback
import aiohttp
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta

from xC4 import *
from xP import JoinSq, OpenCh, MsqSq, ExitSq, PrOtO, OpenSq, ChSq, SendSq
from byte import Encrypt_ID, encrypt_api
from Pb2 import DEcwHisPErMsG_pb2, sQ_pb2

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════
# ERROR LOGGER & SAFE HELPERS
# ═══════════════════════════════════════════════════════════════

def log_error_to_file(error_msg, context="General"):
    """এররগুলোকে bot_error.log ফাইলের ভেতর লগ করে এবং কী কারণে হয়েছে তা বলে দেয়"""
    log_file = "bot_error.log"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    tb = traceback.format_exc()
    
    log_content = f"""
==================================================
[{timestamp}] ERROR IN: {context}
==================================================
Description: {error_msg}
Traceback:
{tb}
--------------------------------------------------
💡 FIX ADVICE: 
- If you see "'int' object is not subscriptable", it means a variable was expected to be a dictionary/object, but Garena server sent it as a raw integer.
- Use safe extraction methods (checking `isinstance(obj, dict)`) instead of direct indexing.
==================================================\n
"""
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_content)
        print(f"⚠️ [Error Logged] Check '{log_file}' for details and fix instructions.")
    except Exception as e:
        print(f"✗ Failed to write log: {e}")


_last_color = None

def get_random_color():
    global _last_color
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]",
        "[FF00FF]", "[00FFFF]", "[FF66CC]", "[FFD700]", "[FFFFFF]",
        "[FFA500]", "[800080]", "[00FF7F]", "[FF1493]",
        "[1E90FF]", "[ADFF2F]", "[DC143C]", "[4B0082]",
        "[7FFF00]", "[FF4500]", "[2E8B57]", "[00BFFF]",
        "[BA55D3]", "[FF69B4]", "[40E0D0]", "[7B68EE]",
        "[8B0000]", "[006400]", "[00008B]", "[2F4F4F]",
        "[191970]", "[800000]", "[008080]", "[ADD8E6]",
        "[90EE90]", "[FFB6C1]", "[E6E6FA]", "[FFFACD]",
        "[F0FFF0]", "[FFE4E1]", "[D8BFD8]", "[39FF14]",
        "[FE019A]", "[00F5FF]", "[BF00FF]", "[FF3131]",
        "[CCFF00]", "[FF10F0]", "[00FFEF]", "[C71585]",
        "[E0115F]", "[B57EDC]", "[FFBF00]", "[DE3163]",
        "[9FE2BF]", "[6495ED]", "[CCCCFF]", "[F4A460]",
        "[FA8072]", "[20B2AA]", "[87CEEB]", "[9370DB]",
        "[FF7F50]", "[6A5ACD]", "[3CB371]", "[A52A2A]",
        "[5F9EA0]", "[D2691E]", "[FF8C00]", "[9932CC]",
        "[8FBC8F]", "[E9967A]", "[00CED1]", "[9400D3]",
        "[FF00FF]", "[66CDAA]", "[000080]", "[BDB76B]",
        "[FFDEAD]", "[FAFAD2]", "[E0FFFF]", "[F5F5DC]",
        "[FF6347]", "[4682B4]", "[EE82EE]", "[9ACD32]",
        "[FFCC00]", "[FF3399]", "[33CCFF]", "[66FF66]",
        "[CC33FF]", "[FF6666]", "[00CC99]", "[3399FF]"
    ]
    if _last_color in colors:
        available = [c for c in colors if c != _last_color]
    else:
        available = colors
        
    _last_color = random.choice(available)
    return _last_color


h1_color = get_random_color()
h2_color = get_random_color()
h3_color = get_random_color()
h4_color = get_random_color()
h5_color = get_random_color() 
h6_color = get_random_color()
h7_color = get_random_color() 
h8_color = get_random_color()


# ═══════════════════════════════════════════════════════════════
# LIKE SYSTEM — Manual only, No auto retry, No DB
# ═══════════════════════════════════════════════════════════════
LIKE_API_URL = "https://new-like-api-two.vercel.app/like"
LIKE_API_KEY = "YASIN"

# ═══════════════════════════════════════════════════════════════
# GLOBALS
# ═══════════════════════════════════════════════════════════════

SPAM_TARGETS_FILE = "spam_targets.json"
ROOM_SPAM_TARGETS_FILE = "room_spam_targets.json"

online_writer = None
whisper_writer = None
spam_running = False
SPAM_INTERVAL = 0.5
bot_uid = None
ToKen = None
region = None
admin_uid = "8089858703"   # 👈 আপনার নিজের ডিফল্ট UID
BLOCK_EMOTE_UID = admin_uid  # dynamic update হবে

current_squad_code = None 
title_loop_running = False
title_loop_task = None
bot_in_squad = False  
magic_bundle_running = False
magic_bundle_task = None
lag_running = False
lag_task = None
pending_ghost_future = None
ghost_team_id = None
ghost_squad_code = None

spm_tasks = {}
ban_task = None
ban_running = False
ban_targets = set()
evo_cycle_running = False
evo_cycle_task = None
freeze_running = False
freeze_task = None

def load_room_spam_targets():
    if os.path.exists(ROOM_SPAM_TARGETS_FILE):
        try:
            with open(ROOM_SPAM_TARGETS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_room_spam_targets():
    with open(ROOM_SPAM_TARGETS_FILE, "w") as f:
        json.dump(room_spam_targets, f)

room_spam_targets = load_room_spam_targets()
room_spam_tasks = {}

fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
msg_spam_running = False
msg_spam_task = None
mg_spam_task = None
reject_spam_running = False
reject_spam_task = None
emote_hijack = False
bot_enabled = True

BOT_UID_FOR_HI = None
BOT_PW_FOR_HI  = None

BLOCK_EMOTE_UID = admin_uid
CACHE_FILE      = "status_cache.pkl"
CACHE_TIMEOUT   = 30

_clan_msg_key = None
_clan_msg_iv = None
_clan_msg_bot_uid = None
_clan_msg_clan_id = None
_clan_message_task = None

BADGE_VALUES = {
    "s1": 1048576,
    "s2": 32768,
    "s3": 2048,
    "s4": 64,
    "s5": 262144
}
BADGE_REQUESTS = 5
PACKET_DELAY_ULTRA_FAST = 0.1

EVO_IDS = [
    909000063, 909000075, 909040010, 909000081, 909039011,
    909045001, 909038012, 909042008, 909051003, 909035012,
    909000098, 909033002, 909037011, 909049010, 909041005,
    909038010, 909033001, 909035007, 909000090, 909000085,
    909000068
]


# ═══════════════════════════════════════════════════════════════
# ⚡ POWERFUL REFRESH SYSTEM (KICK / LEAVE / AUTO-RESET) ⚡
# ═══════════════════════════════════════════════════════════════

async def refresh_bot_state():
    """গ্রুপ থেকে কিক করলে, অটো লিভ নিলে বা ডিসকানেক্ট হলে সমস্ত টাস্ক ও লুপ সম্পূর্ণ ক্লিন রিফ্রেশ করবে"""
    global fast_spam_running, custom_spam_running, msg_spam_running
    global reject_spam_running, freeze_running, evo_cycle_running, ban_running, lag_running
    global room_spam_tasks, spm_tasks, online_writer, whisper_writer
    global ban_task, evo_cycle_task, fast_spam_task, custom_spam_task
    global msg_spam_task, mg_spam_task, reject_spam_task, freeze_task, _clan_message_task, lag_task

    fast_spam_running = False
    custom_spam_running = False
    msg_spam_running = False
    reject_spam_running = False
    freeze_running = False
    evo_cycle_running = False
    ban_running = False
    lag_running = False

    # সকল ব্যাকগ্রাউন্ড টাস্ক বাতিল ও রিসেট করা হচ্ছে
    tasks_to_cancel = [
        ban_task, evo_cycle_task, fast_spam_task, custom_spam_task,
        msg_spam_task, mg_spam_task, reject_spam_task, freeze_task, _clan_message_task, lag_task
    ]
    for task in tasks_to_cancel:
        try:
            if task and not task.done():
                task.cancel()
        except Exception:
            pass
    
    ban_task = None
    evo_cycle_task = None
    fast_spam_task = None
    custom_spam_task = None
    msg_spam_task = None
    mg_spam_task = None
    reject_spam_task = None
    freeze_task = None
    _clan_message_task = None
    lag_task = None

    # সকল রুম ও স্প্যাম টাস্ক ডিকশনারি পরিষ্কার করা হচ্ছে
    for t_dict in [room_spam_tasks, spm_tasks]:
        for k, task in list(t_dict.items()):
            try:
                if task and not task.done():
                    task.cancel()
            except Exception:
                pass
        t_dict.clear()

    # রাইটারগুলো সেফলি ক্লোজ করা হচ্ছে
    for w in [online_writer, whisper_writer]:
        try:
            if w:
                w.close()
        except Exception:
            pass
    online_writer = None
    whisper_writer = None

    print("🔄 [POWERFUL BOT REFRESH] State and background tasks successfully reset without glitches!")

# ═══════════════════════════════════════════════════════════════
# EMOTE SYSTEMS
# ═══════════════════════════════════════════════════════════════

GENERAL_EMOTES_MAP = {}
EMOTE_MAP          = {}
NAME_TO_EMOTE_ID   = {}
EMOTE_MENU         = {}

try:
    with open("emotes.json", "r", encoding="utf-8") as _f:
        _raw = json.load(_f)
    for _num, _info in _raw.items():
        _id   = int(_info["id"])
        _name = str(_info.get("name", f"emote_{_num}"))
        GENERAL_EMOTES_MAP[str(_num)] = _id
        EMOTE_MAP[int(_num)]          = _id
        EMOTE_MENU[str(_num)]         = _name
        _n = _name.lower().strip()
        if _n and not _n.startswith("emote_") and _n not in NAME_TO_EMOTE_ID:
            NAME_TO_EMOTE_ID[_n] = _id
    print(f"✓ Loaded {len(GENERAL_EMOTES_MAP)} emotes from emotes.json")
    print(f"✓ Built {len(NAME_TO_EMOTE_ID)} name→emote mappings")
except Exception as _e:
    print(f"✗ emotes.json load error: {_e}")

try:
    with open("emote_menu.json", "r", encoding="utf-8") as _f:
        EMOTE_MENU = json.load(_f)
except Exception:
    EMOTE_MENU = {}

NAME_EMOTES = {
    "ak": 909000063, "scar": 909000068, "mp40": 909000075,
    "m1014": 909000081, "xm8": 909000085, "famas": 909000090,
    "ump": 909000098, "m1887": 909035007, "woodpecker": 909042008,
    "groza": 909041005, "m4a1": 909033001, "thompson": 909038010,
    "g18": 909038012, "parafal": 909045001, "p90": 909049010,
    "m60": 909051003, "fist": 909037011, "ring": 909050009,
    "heart": 909038004, "love": 909000010, "dance": 909000027,
    "hello": 909000001, "hi": 909000001, "money": 909000129,
    "lol": 909000002, "sad": 909038005, "angry": 909000014,
    "chicken": 909000006, "dab": 909000005, "selfie": 909000040,
    "shower": 909051004, "flower": 909051002, "petals": 909051013,
}
NUMBER_EMOTES = GENERAL_EMOTES_MAP


# ═══════════════════════════════════════════════════════════════
# NEW BOX-STYLE EMOTE MENU SYSTEM (1s Interval / 4 Pages)
# ═══════════════════════════════════════════════════════════════

async def send_box_menu_sequence(XX, uid, chat_id, key, iv):
    """এক সেকেন্ড বিরতিতে পরপর ৪টি বক্স মেনু পেজ পাঠাবে"""
    try:
        items = sorted(EMOTE_MENU.items(), key=lambda x: int(x[0]))
    except Exception:
        items = list(EMOTE_MENU.items())

    total_items = len(items)
    if total_items == 0:
        await safe_send_message(XX, "[B][C][FF0000]✗ Emote menu is empty.", uid, chat_id, key, iv)
        return

    per_page = 5
    total_pages = max(1, math.ceil(total_items / per_page))
    
    # সর্বোচ্চ ৪টি পেজ দেখানোর জন্য লিমিট করা হলো (অথবা যতগুলো পেজ দরকার)
    max_show_pages = min(5, total_pages)

    for page in range(1, max_show_pages + 1):
        start = (page - 1) * per_page
        end   = start + per_page
        page_items = items[start:end]

        # বক্স স্টাইল ডিজাইন
        box_text  = f"[B][C][00FFFF]╔═══════════════╗\n"
        box_text += f"[B][C][FF0000]  🎭 EVO EMOTE MENU [{page}/{max_show_pages}]   \n"
        box_text += f"[B][C][00FFFF]╠═══════════════╣\n"

        for num, name in page_items:
            box_text += f"[C][FFFFFF]║  [FFFF00]{num:<2}[FFFFFF] ➤ [00FF00]{name:<12}[C][FFFFFF]\n"

        box_text += f"[B][C][00FFFF]╚═══════════════╝\n"
        box_text += f"[C][00FF00]⚡ Type: /evo menu for pages"

        # পেজ পাঠানো হচ্ছে
        await safe_send_message(XX, box_text, uid, chat_id, key, iv)
        print(f"📋 Box Menu Page {page}/{max_show_pages} sent")

        # পেজগুলোর মাঝে ১ সেকেন্ড বিরতি
        if page < max_show_pages:
            await asyncio.sleep(1.0)

# ═══════════════════════════════════════════════════════════════
# MASTER MINE EMOTE FUNCTION
# ═══════════════════════════════════════════════════════════════

async def play_custom_emote(emote_id, target_uid=None, key=None, iv=None, region=None):
    global online_writer, bot_uid
    
    if not emote_id:
        return False
        
    try:
        # ইউআইডি না দিলে অটো বটের নিজের ইউআইডি (bot_uid) ব্যবহার করবে
        final_uid = int(target_uid) if target_uid else int(bot_uid)
        
        # যদি লোকাল বা গ্লোবাল থেকে key, iv, region না পাওয়া যায়, তবে গ্লোবাল ভেরিয়েবল চেক করবে
        current_key = key if key is not None else globals().get('key')
        current_iv = iv if iv is not None else globals().get('iv')
        current_region = region if region is not None else globals().get('region', 'BD')
        
        if not current_key or not current_iv:
            print(f"✗ Master Emote Error: Key or IV is missing!")
            return False
        
        # Emote_k ফাংশন কল করা
        emote_packet = await Emote_k(final_uid, int(emote_id), current_key, current_iv, current_region)
        
        if emote_packet and online_writer:
            online_writer.write(emote_packet)
            await online_writer.drain()
            print(f"🎭 [Master Emote Triggered] Emote ID: {emote_id} -> Target: {final_uid}")
            return True
    except Exception as e:
        print(f"✗ Master Emote Error (ID: {emote_id}): {e}")
        
    return False


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def load_spam_targets():
    if os.path.exists(SPAM_TARGETS_FILE):
        with open(SPAM_TARGETS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_spam_targets():
    with open(SPAM_TARGETS_FILE, "w") as f:
        json.dump(list(spam_targets), f)


spam_targets = load_spam_targets()


def get_random_avatar():
    avatar_list = [
        902050001, 902050002, 902050003, 902039016, 902050004,
        902047011, 902047010, 902049015, 902050006, 902049020
    ]
    return random.choice(avatar_list)


def get_random_sticker():
    sticker_packs = [
        ("1200000001", 1, 24),
        ("1200000004", 1, 15),
        ("1200000002", 1, 13),
    ]
    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)
    return f"[1={pack_id}-{sticker_no}]"


def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 3] for i in range(0, len(str(n)), 3))


def fix_num(number):
    fixed = ""
    count = 0
    num_str = str(number)
    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0
    return fixed


def fixnum(num):
    num_str = str(num)
    return "[C]" + "[C]".join(num_str) + "[C]"


def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()


async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    return cipher.encrypt(padded_packet).hex()


async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)


# ═══════════════════════════════════════════════════════════════
# FAST EMOTE SAFE SYSTEM (FIXED & BATCHED)
# ═══════════════════════════════════════════════════════════════

async def fast_emote_spam(tgt_uids, emote_id, key, iv, region):
    global fast_spam_running
    count = 0
    
    while fast_spam_running:
        for tgt_uid in tgt_uids:
            if not fast_spam_running:
                break
            
            try:
                H = await Emote_k(int(tgt_uid), int(emote_id), key, iv, region)
                if online_writer:
                    online_writer.write(H)
                    await online_writer.drain()
            except Exception:
                pass
            
            count += 1
            
            if count % 10 == 0:
                await asyncio.sleep(1.5)
            else:
                await asyncio.sleep(0.2)


# ═══════════════════════════════════════════════════════════════
# AUTH TOKEN BUILDERS & EXTRACTORS
# ═══════════════════════════════════════════════════════════════

def extract_bot_uid_from_auth(auth_token):
    try:
        if isinstance(auth_token, str):
            b = bytes.fromhex(auth_token)
        elif isinstance(auth_token, bytes):
            b = auth_token
        else:
            return None
        if len(b) >= 10:
            uid_val = int.from_bytes(b[2:10], 'big')
            if 1_000_000 < uid_val < 999_999_999_999:
                return str(uid_val)
    except Exception:
        pass
    return None


def build_ob55_online_auth(account_uid, token, kts, key, iv):
    token_bytes = token.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_token = cipher.encrypt(pad(token_bytes, 16))
    opcode = bytes.fromhex("830c")
    uid_bytes = int(account_uid).to_bytes(8, byteorder="big")
    kts_bytes = int(kts).to_bytes(4, byteorder="big")
    len_bytes = len(enc_token).to_bytes(8, byteorder="big")
    return opcode + uid_bytes + kts_bytes + len_bytes + enc_token, enc_token


def create_auth_token_chat(account_id, jwt_token, timestamp, key, iv):
    try:
        K = bytes.fromhex(key) if isinstance(key, str) else key
        V = bytes.fromhex(iv) if isinstance(iv, str) else iv
        jwt_bytes = jwt_token.encode('utf-8')
        ct = AES.new(K, AES.MODE_CBC, V).encrypt(pad(jwt_bytes, AES.block_size))
        uid_b = int(account_id).to_bytes(8, 'big')
        ts_b = int(timestamp).to_bytes(4, 'big')
        len_b = len(ct).to_bytes(4, 'big')
        header = bytes.fromhex('6d19') + uid_b + ts_b + len_b
        return (header + ct).hex()
    except Exception as e:
        print(f"[AUTH TOKEN ERROR] {e}")
        return None


async def cHTypE(H):
    if not H:
        return 'Squid'
    elif H == 1:
        return 'CLan'
    elif H == 2:
        return 'PrivaTe'


async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto


async def GeTSQDaTa(D):
    try:
        return D['5']['data']['1']['data'], D['5']['data']['17']['data'], D['5']['data']['31']['data']
    except KeyError:
        return None, None, None


async def get_colorful_message(message_text, message_number):
    color = "FF0000" if message_number % 2 else "FFFFFF"
    return f"[C][B][{color}]{message_text}"


# ═══════════════════════════════════════════════════════════════
# PACKET BUILDERS
# ═══════════════════════════════════════════════════════════════

async def NewClanChatPacket(message_text, key, iv, clan_id=3102281341):
    fields = {
        1: 16801068917, 2: 18, 4: 1,
        5: {
            1: 16801068917, 2: clan_id, 3: 1, 4: 'YASIN × BHAI',
            5: 1785944381, 7: 6,
            9: {
                1: message_text, 4: 301, 8: '♧YASIN × BHAI♧', 13: '',
                14: {1: 16801068917},
                18: {1: 16801068917, 3: 1, 4: ''}
            },
            10: 'ar', 13: {2: 1, 3: 1}, 14: '',
            16: int(time.time() * 1000)
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', key, iv)


async def AuthClan(clan_id, clan_compiled_data, key, iv):
    if isinstance(clan_compiled_data, str):
        try:
            clan_compiled_data = clan_compiled_data.encode(
                'latin-1', errors='surrogateescape'
            )
        except Exception:
            clan_compiled_data = clan_compiled_data.encode(
                'utf-8', errors='surrogateescape'
            )
    fields = {1: 3, 2: {1: int(clan_id), 2: 1, 4: clan_compiled_data}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1201', key, iv)


async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid':
        return await xSEndMsgsQ(message, chat_id, key, iv, region or "BD")
    elif TypE == 'CLan':
        try:
            return await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
        except Exception as e:
            print(f"Guild old packet error, fallback: {e}")
            return await NewClanChatPacket(message, key, iv, chat_id)
    elif TypE == 'PrivaTe':
        return await xSEndMsg(message, 2, Uid, Uid, key, iv)


async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        whisper_writer.write(PacKeT); await whisper_writer.drain()
    elif TypE == 'OnLine':
        online_writer.write(PacKeT); await online_writer.drain()


async def safe_send_message(chat_type, message, uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            packet = await SEndMsG(chat_type, message, uid, chat_id, key, iv)
            if packet:
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', packet)
                return True
        except Exception as e:
            print(f"✗ Send fail (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False


# ═══════════════════════════════════════════════════════════════
# WELCOME
# ═══════════════════════════════════════════════════════════════

HELP_DELAY = 0.5
WELCOME_DELAY = 1
WELCOME_COOLDOWN = 1800

WELCOME_TEXT = (
    "[B][C][00FFFF]╭[00FFFF]─[00FFFF]╮[00FFFF]╔═══════════╗\n"
    "[C][B][00FFFF]│[00FFFF]ꚠ[00FFFF]│[00FFFF]║[FFFFFF]⚡—͞YASIN × BHAI⚡[00FFFF]║\n"
    "[C][B][00FFFF]╰[00FFFF]─[00FFFF]╯[00FFFF]╚═══════════╝\n"
)
WELCOMED = {}


async def send_welcome(chat_code, key, iv, delay=None):
    now = time.time()
    last = WELCOMED.get(chat_code)
    if last and now - last < WELCOME_COOLDOWN:
        return
    WELCOMED[chat_code] = now
    await asyncio.sleep(WELCOME_DELAY if delay is None else delay)
    await safe_send_message(0, WELCOME_TEXT, None, chat_code, key, iv)


# ═══════════════════════════════════════════════════════════════
# AUTO UID RESOLVER
# ═══════════════════════════════════════════════════════════════
async def resolve_bot_auto_uid(sender_uid, explicit_args=None):
    global bot_uid
    uids = []
    
    if explicit_args:
        for p in explicit_args:
            if p.isdigit() and len(p) >= 7 and not p.startswith("909"):
                if p not in uids:
                    uids.append(str(p))

    sender_str = str(sender_uid)
    if sender_str and sender_str.isdigit() and len(sender_str) >= 7 and not sender_str.startswith("909"):
        if sender_str not in uids:
            uids.append(sender_str)

    if bot_uid and str(bot_uid) not in uids:
        uids.append(str(bot_uid))

    if not uids:
        uids = [str(sender_uid)]

    return uids


# ═══════════════════════════════════════════════════════════════
# CLAN AUTO MESSAGE
# ═══════════════════════════════════════════════════════════════

async def clan_message_loop():
    global _clan_msg_key, _clan_msg_iv, _clan_msg_bot_uid, _clan_msg_clan_id
    try:
        await asyncio.sleep(5)
        if _clan_msg_clan_id and _clan_msg_clan_id > 0 and _clan_msg_key and _clan_msg_iv:
            clan_msg = "[b][c]Dev : [00ffff]YASIN × BHAI"
            await safe_send_message(1, clan_msg, _clan_msg_bot_uid, _clan_msg_clan_id, _clan_msg_key, _clan_msg_iv)
            print(f"[CLAN] Startup message sent to clan {_clan_msg_clan_id}")

        while True:
            await asyncio.sleep(18000)  # 5 hours
            if _clan_msg_clan_id and _clan_msg_clan_id > 0 and _clan_msg_key and _clan_msg_iv:
                clan_msg = "[b][c]Dev : [00ffff]YASIN × BHAI"
                await safe_send_message(1, clan_msg, _clan_msg_bot_uid, _clan_msg_clan_id, _clan_msg_key, _clan_msg_iv)
                print(f"[CLAN] 5-hour message sent to clan {_clan_msg_clan_id}")
    except asyncio.CancelledError:
        print("[CLAN] Message loop cancelled")
    except Exception as e:
        print(f"[CLAN] Message loop error: {e}")


# ═══════════════════════════════════════════════════════════════
# BANNER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

async def base_to_hex(number):
    hex_str = hex(number)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    return hex_str.upper()


async def DEVIL(client_id, key, iv):
    banner_text = f"""   
[B][C][00FF00]★ YASIN × BHAI BOT ★
[FFFF00]━━━━━━━━━━━━━━━━━━━━━━━━━━
[B][C][00FF00]F O L L O W   M E   O N   T I K T O K
[B][C][FFFFFF]@freefire_ob_55
[00008B]━━━━━━━━━━━━━━━━━━━━━━━━━━
[B][C][81DACA]I F   Y O U   D O N T   F O L L O W   M E
[B][C][FF0000]I   W I L L   B A N   Y O U R   A C C O U N T
        """
    fields = {
        1: 5,
        2: {1: int(client_id), 2: 1, 3: int(client_id), 4: banner_text}
    }
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)


async def DEVIL1(client_id, key, iv):
    gay_text = f"""   
[B][C][00FF00]★ YASIN × BHAI BOT ★
[FFFF00]━━━━━━━━━━━━━━━━━━━━━━━━━━
[B][C][00FF00]F O L L O W   M E   O N   T I K T O K
[B][C][FFFFFF]@freefire_ob_55
[00008B]━━━━━━━━━━━━━━━━━━━━━━━━━━
[B][C][81DACA]I F   Y O U   D O N T   F O L L O W   M E
[B][C][FF0000]I   W I L L   B A N   Y O U R   A C C O U N T
        """
    fields = {1: int(client_id), 2: 5, 4: 50, 5: {1: int(client_id), 2: gay_text}}
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)


# ═══════════════════════════════════════════════════════════════
# BADGE COMMAND FUNCTIONS
# ═══════════════════════════════════════════════════════════════

async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] YASIN × BHAI",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56, 97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: int(badge_value)
            },
            32: int(badge_value),
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15, 6, 21, 8, 10, 11, 19, 12, 17, 4, 14, 20, 7, 2, 1, 5, 16, 3, 13, 18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)


async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]✗ Usage: /{cmd} <uid>\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]✗ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
        
    total_requests = BADGE_REQUESTS
    packet_delay = 0.2 
    
    badge_names = {
        's1': 'Craftland Badge 🏆',
        's2': 'New V-Badge 🔥',
        's3': 'Moderator Badge 👮',
        's4': 'Small V-Badge ⚡',
        's5': 'Pro Badge 💎'
    }
    badge_name = badge_names.get(cmd, 'Unknown Badge')
    
    initial_msg = f"[B][C][00FF00]✓ {badge_name} Spam Started!\n[C][FFFFFF]🎯 Target: [FFFF00]{target_uid}\n[C][FFFFFF]📦 Requests: [FFFF00]{total_requests}"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        
        for i in range(total_requests):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(packet_delay)

        success_msg = f"[B][C][00FF00]✓ {badge_name} COMPLETE!\n[C][FFFFFF]🎯 Target: {target_uid}\n[C][FFFFFF]📦 Sent: {total_requests} requests"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]✗ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)


async def Room_Spam(Uid, Rm, Nm, K, V):
    badge_sequence = [1048576, 32768, 2048, 64, 262144]
    badge_index = 0
    for i in range(3000):
        try:
            current_badge_value = badge_sequence[badge_index % 5]
            fields = {
                1: 78,
                2: {
                    1: int(Rm), 2: "iG:[C][B][FF0000] YASIN × BHAI", 3: {2: 1, 3: 1},
                    4: 330, 5: 6000, 6: 201,
                    10: int(get_random_avatar()), 11: int(Uid), 12: 1,
                    15: {1: 1, 2: current_badge_value}, 16: current_badge_value,
                    18: {1: 11481904755, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
                    31: {1: 1, 2: current_badge_value}, 32: current_badge_value,
                    34: {1: int(Uid), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
                }
            }
            spam_packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
            badge_index += 1
            await asyncio.sleep(PACKET_DELAY_ULTRA_FAST)
        except Exception:
            await asyncio.sleep(0.1)
    return True


# ═══════════════════════════════════════════════════════════════
# FULL PACKET BUILDERS
# ═══════════════════════════════════════════════════════════════

async def JoinSq_original(code, K, V):
    skinz = {
        1: 4,
        2: {
            4: "\u0001\u0007\t\n\u000b\u0012\u0019 '",
            5: str(code),
            6: 6,
            8: 1,
            9: {
                1: "08FFF3BE903F27DF0203110111110000006B0003006800169194106F13CF106E4676251411010404dfe9e8b5ca3ca4f96a3119c00000004f03060301cacfa16d",
                2: 130,
                3: "tY_S\u0013\b\u0001M\u0002\u0000T\u0000\u0005\u000e\b\t\u0002\u0000\u0003U\u0003\u0001V\u000fR\u000e\tRQ\u0002\u0004\u0005US\u0003XS\u0005\u0001\u0002\u0011\u0001\u0002JuTAEN\u001e\u0002\u001c\u0002\u001f\u0013\b\u0003M\u001cDbz_Q@}p_QOgsC\u001dYVI\u0004UAAj_ga\u0004\u0012\u0000K\u001d\u0007_t\u0019b\bCx\u0002UeGat\u001fTTCBLER`\u0006\u0001\r\f\u0012\u0006\u0005N^^\u0002acH~r\u0004_\u0003RO|\u000bcd_@~`Rnqrgh\n\u0015\nL\\Nh\u0000~G\u000et\u0000eb]VQ\u0006t^F[ZIGxCdZD\u000b\u0011\u0002OA~LP@\u000fcSDyATQApaT^{|wa]\\\u0001E\u000f\u0013\nJfxve}\u0004J\u0003c{YL\u0007^^yDYQf\bhe\u0005_wg\r\u0010\u0007\bEHpX@||\u0002Z\\uTGyA\u0001JP\u0005t~VkTE\u0000J\\\u000b\u0013\nMr\u0018zTzK}qE]vnvwROuheYvwduvQ\r\u001a\u0005M\u0006z\u001dfXfzvHFc~dXUz}O\u001aB\u0005t\u0002i\u001co_\u0004\u0012\u0003\u0007J\u0006b\u0003\u000eqlfvbEstgu~wB\u0001v@`yI\u0002ZPx\f\u0014\u0003NR\u0002yBZvuD_cd\u0004q]lH]\u0007bD}pCe\t\u0004t\n",
                4: "w^_R", 6: 11, 7: "\u0014\u0004aqrg\u0015\u0013", 8: "1.132.1", 9: 3, 10: 2,
                11: "\u0003bbSQ6wxegh9qAdV2KyoVleA17yPmYF+yTnOrl+JMknmppeUBe5ZsiHueP2mZZ4KOs6b2Ail1S9z3qIeU9hGFZ2M6PP39/zjIc/RFVPAkgDagySswMVmYaPhkzU5IqNPow2843fyQUz9xI10NdMhl1WiI4Y6wCXBotiUS9wSgujQ4j0fWXUyklCxBWo8r27hyoGSVrPdTPXFMnJJpPRRFFmWqc3fWvMg+BNfxSRJOZRSrkzG0nNvSIJ4uZB2pqAlHIPEYx7bI6zsgwUVDiLZJKTUTyuCGbOd1DegDUFfazFesTG1LJknT5WhgzCsrBIy+f2l+LeJe5DW7wEwNaHambM7ECXcJcLIhB9kJJsW0tFvXkk3HSdcQ8N1K6wjSKWhpkW0kV8Zrjj0jkhS/7AZ6T9GJRIA827YDtTorBvbx1UkXjYrqYI1nSa2GaMexGnqlurc5DE3v1R+mUBI9GqmjEPgTSYVBxyeCdQMHaMXGtspAhvkiO84ToU87sP45pylDEfFOVoc/rcmdzWeqlYPsv6txKRtIHcb0cO+MoVShoU8ZUVRDF3znbqzVrscPIfplBaa79lwvQqzRubLl9XY="
            },
            11: {1: "IDC4", 2: 281, 3: "ME"},
            13: "fr", 16: "7OR\u0019", 20: "\b\u0015", 27: "\bH\u0010\u0003"
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(skinz)).hex(), '0515', K, V)


async def YASIN_BHAI_Accepted(uid, code, K, V, region):
    fields = {
        1: 4,
        2: {
            1: int(uid), 3: int(uid),
            4: "rYUW\u0017\t\u0007NR\u000f\u0005\u0004\\W\u0002\u000fV\u0004TPQ\u0003\u000f\u0005\u0004]\u0005\u000b\u0000\u0002W\u0005\r\nVY\u0004\u0007\u0007\u0007\u0017\u0001\bNQ\fS\u0005\u000e\u0006\f\u0005\rT\u0002\r\u0000TS\u0007U\u0004X\u0006RY\u0005\u0003\u0003SW\u0000\u000eQ\u0000^\u0014\u0003\u0004JXS\u000f\u0000g{gqfePblEZJp{_xU\bmQW\f\u0007\u000f\u0015\u0007H\\U^CHXh@Ax`\u000f~\rPN~Nz\\\u001fr_ckPU\u000b\u0015\u0005\u0003Ekfp\u007fcY\u0001nWV\u0002\u0005azE~N\u0007HTg\u0007w}@\u0002{\t\u0013\u0001NeNP]DUf|]ugINs{\u0001\\rAgB_\u0004fA]\u0004\r\u001a\u0000HpOv\\\u0005|gS\u0019\\A\u007fWW\u0003\u007fTqFGi\u0004Qr\u0019dW\u0004\u0011\rD\u0002yeZ]A\u0016a\u0007Ungeg\u0007E\\P\u001b\u000b\u0004\u0005dd\ff\r\u000f\u0017\t\u000fNRyZd\u0012tZ\fe\u0007AGv\u007fw]{P\u001c\u007f\u000ff\u0005ZJK\u0004\u0005\u0014\u0001Jgq\u001frymsB\u0001\u000fd`\u001bj~[}\u0004SDZ|IxKB\u0000\n\u0011\u0002J^`tjYN\u0007WQdE[PQ\u0002_{VP`S\t\u007f\u001dP\n\u000f\u000f\u0015\u0004\u0004L{V\u0003@yP[rgJ{Hpk\u0001\u000bw\u0001Agt_\u0003HxPc\u000b\u0017\u0005E`y\ngWoy\u0006S{A\u001b``Y\u0002Xzw}dDWOKsg\t\u0013\u000eNf\u000e\\`\u0005AwJc\u0003BM\u0001^\u0000R\u0002Qoh]tbS~`G\r\u001a\u0004HibAQ\u000f^XNt~kDUWaeaNqcLQ]Py[G\u0004",
            8: 1,
            9: {
                1: "08FBA33CFF105FDD02030A01111100000003000100020000B687046B0D6D2083467625141101030175a63c900e748c3f6a311e04000000ff00040202cacfa16d",
                2: 197,
                3: "735154531406054a035305025a0e50560f5100040250020f5e0401520653000303505e0d520302501500064d705548424e1f051a001e12040a441d45677f5a56477574565e4f6274451d585849005a4f456d5b64670c1400496d017842740c670100040069536e72586c02016e657e566b524403081500044d0d515b637f757c19095c7c510b00417f565e5e066f5b584d6e02400a160e4d58496d0177400e750763605c575d0f7d5f475e5f4c407f4b60534b0b140549751e66407a4860726e44400e6103557e515c646f43577106077b60051b0f4b4e474e58457e4f615c01406000051e0361516e7b67614e040102540c1609004a0e40730f62517f446a135179507e706850547f7e7a67795553597c0a1206445b456640046265725c4d505d446d50737b7c42035970486370645e0b12034d506f5c7a1c554f574b0e765a0f0a7364505203477569456c6c420f0a1604014b647149136c186f795f5d78755e550e7842545e53747b08705f7f5d0a14004a08666b5a5b5f00045c7f5e584d72584262705f56055c61475564790515004b76514178587f52797a0f077a070953507d7f4d784f794f667b4256081b0e4a75627d4778417a06717574747c4c78557b4b7a0a697f0e714573600a",
                4: "{Y_R", 6: 13, 7: "1c6f017306741513", 8: "2.126.22", 9: 2, 10: 1,
                11: "036262535136784d584e38742b416456324b796f566c6537392f763672324d4773683377706379634f6b6b6f7447397934523930517432797246474c464c624c777a7747344d4d5257623146756d2b6556777a62597736743973492b787059612f55596e43465a59485235713348705830306c485a6f3632565145574e7145705866414c38734a754646575247386d376f5444566a4c484c576e714c52576f4e653236437a734c346a4144482b71694b55384d71476c5936546669544863716c487a345568463869396a365233366d49774b71746c36714f797568513854367945714b69742f45466d2b3636634b787649304f384d6c41385166454b6253467366477a2f30684e6a543873305369722f3962635a2f4679376c752f61632f366765704d415734566b442b36374f535756473665377a775a79312b797a42334b70632b7571782b577437414d39727761644439575765704570567849526d66654f5847627775787a68574b5664344c49586f415a364b387063647450627953575857455135706a542b653669365a2f6177444a3179356f774d5a534f64487262392b7877424a4d444f7848565a7a483372547a30314a316738517675466b656c3042433746473630683456427041494457487956684e794b4f5145507139467a4a6272686b316146306768766578512f6a2f484767426a5268675134645243372b477a5a687a2b77505967376454746f2b494d56363774642b54435653314234346b4148395a6d415872763758615941626477644e664f533170484875736b7336346f72463452534d3772656345417661484e61484854314c5545686e786a5a616d4d4f303d"
            },
            10: str(code),
            11: {1: "IDC3", 2: 84, 3: "BD"},
            13: "en", 16: "374f5219",
            20: {1: 21}, 23: "a_1477547277882450725", 27: {1: 2, 2: 8}
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def accept_squad_invite(group_id, joiner_account_id, invitee_type, key, iv, region="bd"):
    fields = {1: 38, 2: {1: int(group_id), 2: int(joiner_account_id), 8: int(invitee_type)}}
    pkt_type = '0514' if region.lower() == "ind" else ('0519' if region.lower() == "bd" else '0515')
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), pkt_type, key, iv)


async def leave_channel_req(channel_id, channel_type, key, iv):
    fields = {1: 4, 2: {1: int(channel_id), 2: int(channel_type), 3: "en"}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', key, iv)


async def SPamSqForSpm(Uid, K, V):
    same_value = random.choice([4096, 16384, 8192])
    fields = {
        1: 33,
        2: {
            1: int(Uid), 2: "ME", 3: 1, 4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] @freefire_ob_55",
            7: 330, 8: 1000, 10: "ME",
            11: bytes([49,97,99,52,98,56,48,101,99,102,48,52,55,56,97,52,52,50,48,51,98,102,56,102,97,99,54,49,50,48,102,53]),
            12: 1, 13: int(Uid),
            14: {1: 2203434355, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
            16: 1, 17: 1, 18: 312, 19: 46,
            23: bytes([16, 1, 24, 1]),
            24: await xBunnEr(), 26: "", 28: "",
            31: {1: 1, 2: same_value}, 32: same_value,
            34: {1: int(Uid), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
        },
        10: "en", 13: {2: 1, 3: 1}
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def GhostPakcet(player_id, nm, secret_code, key, iv):
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id), 2: 1159,
                3: f"[b][c]{get_random_color()}{nm}", 5: 12, 6: 999, 7: 1,
                8: {2: 1, 3: 1}, 9: 3
            },
            3: secret_code
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', key, iv)


async def xSKINZxLag(K, I):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 15, 2: {1: 804266360, 2: 1}})).hex(), '0515', K, I)


async def xBaNchaTxSkInZ(uidd, K, V):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 3, 2: {1: int(uidd), 3: "fr", 4: "1750728024661459697_3qind8eeqs"}})).hex(), '1215', K, V)


async def create_lw5_packet1(key, iv):
    fields = {
        1: 1,
        2: {
            2: "0b", 3: 43, 4: 1, 5: "en",
            8: {1: "IDC3", 2: 109, 3: "BD"},
            9: 1, 10: "01090a0b12192027", 11: 1, 13: 1,
            14: {
                1: "08FBA33CFF11B915020FEB099999000002BF000C02B3024798E574700E9B7471467625142200004375a63c900e748c3f6a311e04000000ff42002b09cacfa16d",
                2: 1023,
                3: "715c5f561b06054a03530500570555590f5100040250000255010e520653000303525306570c02501500064d72584347411f051a001e1206074f184a677f5a564775765b554a6d74451d58584902574440625b64670c14004b600a7d4d740c670100040264586b7d586c02016e657c5b60574b03081500044d60795258726206047f04600f405b18710347746242085f055442530a160e4d58496f0c7c4501750763605c575f02765a485e5f4c407f4b625e400e1b054973535b40655e5151566e6507797e6b47727a1c6e455762637d650708100a447e704c1e530200437a604b66065d595f58444c5a06095a6c44677a0c14040b4f705b7d75624374067840416d60067353017f5972506356014354680a12044950406940046265725c4f5d56416250737b7c42035b7d43667f645e0b12034d5262577f13554f574b0e76580201766b50520347756947616747000a1604014b6473441869176f795f5d78755c58057d4d545e53747b08725274580514004a08666b585654050b5c7f5e584d725a4f69755056055c61475566740e100f4b76514178587d5f727f00077a070953507f72467d40794f667b42560a16054f7a627d4778417a047c7e717b7c4c78557b4b7807627a01714573600a",
                4: "{Y_R", 6: 13, 7: "136601706b6f54001513", 8: "2.126.20", 9: 2, 10: 1,
                11: "0362625351367a6e2f56386835416456324b796f566c576a3265735033734558335070623443526c656c47355732327673496e477a425a49677375684a664336766942532f4277526d3632374a624a724c562b586b664c516c674942463461566454e34473869494c456e4c7643347754354670754e66444b7746367765466d675a2b2b36704d57694549677343415756457144554a454d737271515a306b544266635a45334959485661774d5332622b4f6b5a477a755171576e3645624c6a3932646c31307754614d55714e355556796742506f454572376651673249754332545a773333796c71493838627562512f6e425072353577785436617955544d63624d2b756d4542345a736c5165504d58725365737864622f30577967786849384a352f73484f685730494a49643450534b6d6a41734b315251495257634c35646355554b457a6d33334475735877384a5267483364412b66414b336433726a4241317954327451326c2f73584c6d4b4b6456707062624b4f3272694c384947382b634a3863506533314241456d517876744f495631323658394c4b35414c6a38533631526d6159617077676e4579724a5a7a624d4c596c3542554b6d7934473546334c6152454c4e6d726a684f557065462f39686f64356c526378623250777244566d455665715355764a456548644e375279344c707035563466392f6f6d3837426b5a6c6159364c5439396b5579554266434c5538647a4a2b43655a35784a44585064654a51686e46496945506e7a506d32334b637a2b512b384a51307a522b5a5a41762b694873454748516a536e61467862356a517a526c374f5a793241385731437263513d"
            },
            19: 329, 21: "374f5219", 24: {1: 21}, 27: "a_1477547277882450725"
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', key, iv)


async def create_lw5_packet2(key, iv):
    return await GeneRaTePk(
        (await CrEaTe_ProTo({1: 17, 2: {1: 17165783357, 2: 1, 3: 4, 4: 6100, 5: b'\x1a', 8: 5, 13: 329}})).hex(),
        '0515', key, iv
    )


async def send_sticker_packet(target_uid, chat_id, key, iv, nickname="YASIN × BHAI"):
    try:
        sticker_value = get_random_sticker()
        fields = {
            1: 1,
            2: {
                1: int(target_uid), 2: int(chat_id),
                5: int(time.time()),
                8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}", 2: get_random_avatar(), 4: 330, 5: 827001007,
                    8: "YASIN × BHAI TEAM", 10: 1, 11: 66, 12: 66, 13: {1: 2},
                    14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"}
                },
                10: "en", 13: {2: 2, 3: 1}, 14: {}
            }
        }
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        encrypted = await encrypt_packet(packet_hex, key, iv)
        pl = len(encrypted) // 2
        hl = f"{pl:04x}"
        prefix = "121500" + ("0" * (6 - len(hl)))
        return bytes.fromhex(prefix + hl + encrypted)
    except Exception as e:
        print(f"✗ Sticker error: {e}")
        return None


async def animation_packet(animation_id, key, iv):
    fields = {1: 88, 2: {1: {1: int(animation_id)}}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    pl = len(encrypted) // 2
    hl = format(pl, 'x')
    final = "051500" + "0" * (6 - len(hl)) + hl + encrypted
    return bytes.fromhex(final)

async def magic_bundle_loop(chat_id, key, iv, region, XX, uid):
    global magic_bundle_running
    magic_bundle_running = True
    
    # আপনার টেস্ট করা সঠিক সময়সহ বান্ডেল ডাটা
    bundle_data = [
        (914000003, 3.0),   # ১ নম্বর বান্ডেল (আগে ৪.৫ ছিল)
        (914038001, 3.0),   # ২ নম্বর বান্ডেল (আগে ৪.৫ ছিল)
        (914042001, 3.0),   # ৩ নম্বর বান্ডেল (আগে ৪.৯ ছিল)
        (914039001, 5.0),   # ৪ নম্বর বান্ডেল (আগে ৬.৯ ছিল)
        (914000002, 5.2),   # ৫ নম্বর বান্ডেল (আগে ১০.০ ছিল)
        (914044001, 4.0),   # ৬ নম্বর বান্ডেল (আগে ১০.০ ছিল)
        (914047002, 4.1),   # ৭ নম্বর বান্ডেল (আগে ১০.০ ছিল)
        (914048001, 4.4),   # ৮ নম্বর বান্ডেল (আগে ১০.০ ছিল)
        (914051001, 4.0),   # ৯ নম্বর বান্ডেল (আগে ১০.০ ছিল)
        (914053001, 4.0),   # ১০ নম্বর বান্ডেল (আগে ১০.০ ছিল)
    ]
    
    total = len(bundle_data)
    await safe_send_message(XX, f"[B][C][00FF00]✨ Magic Bundle Cycle Started ({total} bundles)!", uid, chat_id, key, iv)
    
    for idx, (bid, wait_time) in enumerate(bundle_data):
        if not magic_bundle_running:
            break
        try:
            # ১. প্রথমে অ্যানিমেশন প্যাকেট পাঠানো
            anim_pkt = await animation_packet(bid, key, iv)
            if anim_pkt and online_writer:
                online_writer.write(anim_pkt)
                await online_writer.drain()
            
            print(f"✨ [MAGIC] Playing animation {idx+1}/{total}: {bid} (Duration: {wait_time}s)")
            
            # ২. এনিমেশন শেষ হওয়া পর্যন্ত নির্ধারিত সময় অপেক্ষা করা
            await asyncio.sleep(wait_time)
            
            # ৩. এনিমেশন শেষ হওয়ার ঠিক সাথে সাথে (২ মিলিসেকেন্ড পরে) লুক চেঞ্জার কল করা
            await asyncio.sleep(0.001)
            
            b_pkt = await Look_Changer(bid, key, iv, look_type=1, region=region)
            if b_pkt and online_writer:
                online_writer.write(b_pkt)
                await online_writer.drain()
                
            print(f"✨ [MAGIC] Applied bundle {idx+1}/{total}: {bid}")
            
        except Exception as e:
            print(f"✗ Magic bundle error for {bid}: {e}")
        
        # পরবর্তী বান্ডেলে যাওয়ার আগে ১ সেকেন্ড বিরতি
        if idx < total - 1:
            await asyncio.sleep(1.0)
    
    magic_bundle_running = False
    await safe_send_message(XX, f"[B][C][00FF00]✨ Magic Bundle Cycle Finished Successfully!", uid, chat_id, key, iv)

async def Look_Changer(bundle_id, key, iv, look_type=1, region="bd"):
    fields = {1: 88, 2: {1: {1: bundle_id, 2: look_type}, 2: 2}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    hl = await DecodE_HeX(len(encrypted) // 2)
    if region.lower() == "ind":
        pt = "0514"
    elif region.lower() == "bd":
        pt = "0519"
    else:
        pt = "0515"
    if len(hl) == 2:
        h = f"{pt}000000"
    elif len(hl) == 3:
        h = f"{pt}00000"
    elif len(hl) == 4:
        h = f"{pt}0000"
    elif len(hl) == 5:
        h = f"{pt}000"
    else:
        h = f"{pt}000000"
    return bytes.fromhex(h + hl + encrypted)


async def banecipher(target_uid, key, iv):
    banner_text = ".\n.\n.\n[b][FF0000]YASIN × BHAI[FFFFFF] ⚡\n.\n.\n."
    fields = {1: 5, 2: {1: int(target_uid), 2: 1, 3: int(target_uid), 4: banner_text}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    hl = await DecodE_HeX(len(encrypted) // 2)
    if len(hl) == 2:
        f = "0515000000"
    elif len(hl) == 3:
        f = "051500000"
    elif len(hl) == 4:
        f = "05150000"
    elif len(hl) == 5:
        f = "0515000"
    else:
        f = "0515000000"
    return bytes.fromhex(f + hl + encrypted)


async def banecipher1(target_uid, key, iv):
    gay_text = ".\n.\n.\n[b][FF0000]YASIN × BHAI ⚡[FFFFFF]\n.\n.\n."
    fields = {1: int(target_uid), 2: 5, 4: 50, 5: {1: int(target_uid), 2: gay_text}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    hl = await DecodE_HeX(len(encrypted) // 2)
    if len(hl) == 2:
        f = "0515000000"
    elif len(hl) == 3:
        f = "051500000"
    elif len(hl) == 4:
        f = "05150000"
    elif len(hl) == 5:
        f = "0515000"
    else:
        f = "0515000000"
    return bytes.fromhex(f + hl + encrypted)

async def title_spam_loop(target_uid, chat_id, key, iv, region, XX, title_id):
    global title_loop_running, whisper_writer
    title_loop_running = True
    
    MY_EMOTE_ID = 909000002  # আপনার পছন্দের ইমোট আইডি
    
    while title_loop_running:
        try:
            # ১. টাইটেল পাঠানো
            title_packet = await noob(target_uid, chat_id, key, iv, nickname="YASIN × BHAI", title_id=title_id, emote_id=0)
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
            
            # ২. মাস্টার ইমোট ফাংশনে key, iv, region সহ কল করা
            await play_custom_emote(MY_EMOTE_ID, target_uid=bot_uid, key=key, iv=iv, region=region)
            
            # ১.৫ সেকেন্ড বিরতি
            await asyncio.sleep(1.5)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Title loop error: {e}")
            await asyncio.sleep(1.5)

async def convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="YASIN × BHAI", title_id=None):
    try:
        if title_id is None:
            available_titles = [905090075, 904990072, 904990069, 905190079, 904090014, 904090015,
                                904090024, 904090025, 904090026, 904090027, 904990070, 904990071]
            title_id = random.choice(available_titles)
        fields = {
            1: 1,
            2: {
                1: int(target_uid), 2: int(chat_id),
                5: int(time.time()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}", 2: get_random_avatar(), 4: 330, 5: 827001007,
                    8: "YASIN × BHAI TEAM", 10: 1, 11: 1, 13: {1: 2},
                    14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"}
                },
                10: "en", 13: {2: 2, 3: 1}, 14: {}
            }
        }
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        encrypted = await encrypt_packet(packet_hex, key, iv)
        pl = len(encrypted) // 2
        hl = f"{pl:04x}"
        prefix = "121500" + ("0" * (6 - len(hl)))
        return bytes.fromhex(prefix + hl + encrypted)
    except Exception as e:
        print(f"✗ Title error: {e}")
        return None


async def noob(target_uid, chat_id, key, iv, nickname="YASIN × BHAI", title_id=None, emote_id=909000002):
    try:
        if title_id is None:
            available_titles = [904090014, 904090015, 904090024, 904090025, 904090026, 904090027, 904990070, 904990071, 904990072]
            title_id = random.choice(available_titles)
        
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: int(emote_id),
                    8: "YASIN × BHAI - C4",
                    10: 1,
                    11: 1,
                    13: {1: 2},
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {2: 2, 3: 1},
                14: {}
            }
        }
        
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        return final_packet
    except Exception as e:
        print(f"✗ Conversion error: {e}")
        return None


async def send_all_titles_sequentiallly(uid, chat_id, key, iv, region, chat_type, inviter_uid=None, mode="9"):
    titles_9 = [
        {"title": 904090014, "emote": 909000002},
        {"title": 904090015, "emote": 909000002},
        {"title": 904090024, "emote": 909000002},
        {"title": 904090025, "emote": 909000002},
        {"title": 904090026, "emote": 909000002},
        {"title": 904090027, "emote": 909000002},
        {"title": 904990070, "emote": 909000002},
        {"title": 904990071, "emote": 909000002},
        {"title": 904990072, "emote": 909000002}
    ]
    
    titles_12 = [
        {"title": 905090075, "emote": 909000002},
        {"title": 904990072, "emote": 909000002},
        {"title": 904990069, "emote": 909000002},
        {"title": 905190079, "emote": 909000002},
        {"title": 904090014, "emote": 909000002},
        {"title": 904090015, "emote": 909000002},
        {"title": 904090024, "emote": 909000002},
        {"title": 904090025, "emote": 909000002},
        {"title": 904090026, "emote": 909000002},
        {"title": 904090027, "emote": 909000002},
        {"title": 904990070, "emote": 909000002},
        {"title": 904990071, "emote": 909000002}
    ]
    
    title_emote_pairs = titles_12 if str(mode) == "12" else titles_9
    total_titles = len(title_emote_pairs)
    
    target_for_msg = int(inviter_uid) if inviter_uid and int(inviter_uid) != 0 else int(uid)
    
    target_uids = [int(uid)]
    if inviter_uid and int(inviter_uid) != 0 and int(inviter_uid) != int(uid):
        target_uids.append(int(inviter_uid))
    
    try:
        start_msg = f"[B][C][FFFF00] এই শা🤫লা বো👽কা👽চু👽দা তুই YASIN × BHAI কে নুব বলছিস তোর মাকে কন👽ডম দিয়ে চু👽দি \n\n"
        await safe_send_message(chat_type, start_msg, target_for_msg, chat_id, key, iv)
        
        await asyncio.sleep(2)
        
        for index, pair in enumerate(title_emote_pairs):
            title_number = index + 1
            title_id = pair["title"]
            
            # আগের সেই (index % 2 == 0) শর্ত বাদ দেওয়া হয়েছে, এখন প্রতিটা টাইটেলের সাথেই ইমোট যাবে!
            current_emote = pair["emote"]
            
            for target in target_uids:
                # ১. টাইটেল প্যাকেট পাঠানো
                title_packet = await noob(target, chat_id, key, iv, nickname="YASIN × BHAI", title_id=title_id, emote_id=current_emote)
                if title_packet and whisper_writer:
                    whisper_writer.write(title_packet)
                    await whisper_writer.drain()
            
            # ২. প্রতিটা টাইটেলের সাথেই ইমোট ট্রিগার হবে
            if current_emote > 0:
                try:
                    # [ক] মাস্টারমাইন্ড ফাংশন কল: বটের নিজের জন্য
                    await play_custom_emote(current_emote, key=key, iv=iv, region=region)
                    
                    # [খ] ইনভাইটদাতার জন্য ইমোট প্যাকেট
                    if inviter_uid and int(inviter_uid) != 0:
                        inviter_emote_pkt = await Emote_k(int(inviter_uid), int(current_emote), key, iv, region)
                        if inviter_emote_pkt and online_writer:
                            online_writer.write(inviter_emote_pkt)
                            await online_writer.drain()
                except Exception as e:
                    print(f"Title Emote Error: {e}")
            
            print(f"✓ Sent title {title_number}/{total_titles}: ID {title_id} with emote {current_emote}")
            
            # আগের মতো নির্দিষ্ট বিরতি বা ডিলে (২ সেকেন্ড) ফিরিয়ে আনা হলো, যাতে একটা টাইটেল যাওয়ার ২ সেকেন্ড পর আরেকটা যায়!
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        await asyncio.sleep(2)
        
        completion_msg = f"[B][C][FFFF00] মা💀দা💀রচো💀দ এ💀ইসব টাই💀টেল দিয়ে দেখাছ রে💀ন্ডি মা🤫গির পো🤫লা\n"
        await safe_send_message(chat_type, completion_msg, target_for_msg, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]✗ Error sending titles: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, target_for_msg, chat_id, key, iv)


# ═══════════════════════════════════════════════════════════════
# LOOPS
# ═══════════════════════════════════════════════════════════════

async def spm_loop(uid, key, iv, interval=0.5):
    while True:
        try:
            if online_writer is not None:
                packet = await SPamSqForSpm(uid, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet)
            else:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"spm_loop error for {uid}: {e}")
        await asyncio.sleep(interval)

async def lag_team_loop(team_code, key, iv, region, max_times=10):
    """Controlled join/leave loop with safe anti-cheat delay and exact count limit"""
    global lag_running, lag_task
    count = 0
    
    print(f"🚀 [LAG START] Target Team: {team_code} | Target Cycles: {max_times}")
    
    while lag_running and count < max_times:
        try:
            # Join the team using stable JoinSq_original
            join_packet = await JoinSq_original(team_code, key, iv)
            if online_writer and join_packet:
                online_writer.write(join_packet)
                await online_writer.drain()
            
            # Safe delay to prevent Garena anti-cheat drop (0.15s)
            await asyncio.sleep(0.15)  
            
            # Leave the team safely
            try:
                leave_packet = await ExitSq(int(bot_uid), key, iv)
            except Exception:
                leave_packet = await ExiT(None, key, iv)
                
            if online_writer and leave_packet:
                online_writer.write(leave_packet)
                await online_writer.drain()
            
            count += 1
            print(f"Lag cycle #{count}/{max_times} completed for team: {team_code}")
            
            # Delay between cycles to bypass anti-ban system
            await asyncio.sleep(0.2)  
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            await asyncio.sleep(0.3)
            
    # Target complete হলে অটো বন্ধ হয়ে যাবে
    lag_running = False
    print(f"✨ [LAG COMPLETED] Successfully finished {count} cycles for team {team_code}")


async def ban_loop(key, iv, interval=2.0):
    global ban_running, ban_targets
    ban_running = True
    while ban_running:
        if online_writer is not None and ban_targets:
            for uid in list(ban_targets):
                try:
                    ban_pkt = await xBaNchaTxSkInZ(uid, key, iv)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ban_pkt)
                except Exception as e:
                    print(f"Ban error / Connection dropped: {e}")
                    await asyncio.sleep(5.0)
        await asyncio.sleep(interval)


async def evo_gun_cycle(uids, evo_ids_list, key, iv, region):
    global evo_cycle_running
    cc = 0
    while evo_cycle_running:
        cc += 1
        for emote_id in evo_ids_list:
            if not evo_cycle_running:
                break
            for uid_str in uids:
                try:
                    H = await Emote_k(int(uid_str), int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                except Exception as e:
                    print(f"Emote error: {e}")
            if evo_cycle_running:
                for i in range(5):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        if evo_cycle_running:
            await asyncio.sleep(2)


async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    global custom_spam_running
    count = 0
    while custom_spam_running and count < times:
        try:
            H = await Emote_k(int(uid), int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)
        except Exception:
            break


async def reject_spam_loop(target_uid, key, iv):
    global reject_spam_running
    count = 0
    while reject_spam_running and count < 150:
        if online_writer is None:
            await asyncio.sleep(1)
            continue
        try:
            p1 = await banecipher1(target_uid, key, iv)
            p2 = await banecipher(target_uid, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p2)
            count += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Reject error: {e}")
            break
    return count


async def room_spam_worker(tgt, rid, key, iv, chat_type, chat_id, uid):
    global room_spam_tasks, room_spam_targets
    sent_count = 0
    
    await safe_send_message(
        chat_type,
        f"[B][C][00FF00]🚀 Room Spam Started!\n[C][FFFFFF]Target UID: [FFFF00]{tgt}\n[C][FFFFFF]Room ID: [FFFF00]{rid}\n[C][FFFFFF]Status: Unlimited Spaming ⚡",
        uid, chat_id, key, iv
    )
    
    badge_sequence = [1048576, 32768, 2048, 64, 262144]
    badge_index = 0
    
    while rid in room_spam_tasks:
        try:
            current_badge_value = badge_sequence[badge_index % 5]
            fields = {
                1: 78,
                2: {
                    1: int(rid), 2: "iG:[C][B][FF0000] YASIN × BHAI", 3: {2: 1, 3: 1},
                    4: 330, 5: 6000, 6: 201,
                    10: int(get_random_avatar()), 11: int(tgt), 12: 1,
                    15: {1: 1, 2: current_badge_value}, 16: current_badge_value,
                    18: {1: 11481904755, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
                    31: {1: 1, 2: current_badge_value}, 32: current_badge_value,
                    34: {1: int(tgt), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
                }
            }
            spam_packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
            sent_count += 1
            badge_index += 1
            
            if sent_count % 200 == 0:
                await safe_send_message(
                    chat_type,
                    f"[B][C][00FF00]⏳ Room Spam Total: {sent_count} sent...",
                    uid, chat_id, key, iv
                )
                
            await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Room spam worker error: {e}")
            await asyncio.sleep(0.1)
            
    await safe_send_message(
        chat_type,
        f"[B][C][FF0000]🛑 Room Spam Stopped! Total Sent: {sent_count}",
        uid, chat_id, key, iv
    )


async def msg_spam_loop(message_text, times, chat_id, key, iv, region):
    global msg_spam_running
    count = 0
    while msg_spam_running and count < times:
        try:
            colorful = await get_colorful_message(message_text, count + 1)
            msg_packet = await xSEndMsgsQQ(colorful, int(chat_id), key, iv)
            if msg_packet and whisper_writer:
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                count += 1
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Msg error: {e}")
            break
    return count


async def xSEndMsgsQQ(Msg, id, K, V):
    fields = {
        1: id, 2: id, 4: Msg, 5: 1756580149, 7: 2, 8: 904990072,
        9: {
            1: "YASIN × BHAI - C4", 2: get_random_avatar(), 4: 330, 5: 1001000001,
            8: "YASIN × BHAI - C4", 10: 1, 11: 1, 13: {1: 2},
            14: {1: 1158053040, 2: 8, 3: b"\x10\x15\b\n\u000b\x15\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}
        },
        10: "en", 13: {2: 2, 3: 1}
    }
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)


async def send_wave_messages(message_text, repeats, chat_id, key, iv, region):
    global msg_spam_running
    count = 0
    total_cycles = 0
    while msg_spam_running and total_cycles < repeats:
        try:
            for i in range(1, len(message_text) + 1):
                if not msg_spam_running:
                    break
                partial = message_text[:i]
                colorful = await get_colorful_message(partial, i)
                msg_packet = await xSEndMsgsQ(colorful, int(chat_id), key, iv)
                if msg_packet and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                    count += 1
                    await asyncio.sleep(0.1)
            for i in range(len(message_text) - 1, 0, -1):
                if not msg_spam_running:
                    break
                partial = message_text[:i]
                colorful = await get_colorful_message(partial, i)
                msg_packet = await xSEndMsgsQQ(colorful, int(chat_id), key, iv)
                if msg_packet and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                    count += 1
                    await asyncio.sleep(0.1)
            total_cycles += 1
        except Exception as e:
            print(f"Wave error: {e}")
            break
    return count, total_cycles


async def freeze_emote_spam(uid, key, iv, region, chat_type, chat_id, sender_uid):
    global freeze_running
    FREEZE_EMOTES = [909052010, 909052010, 909052010]
    cycles = 0
    while freeze_running and cycles < 10:
        if online_writer is None:
            await asyncio.sleep(1)
            continue
        for emote_id in FREEZE_EMOTES:
            if not freeze_running:
                break
            try:
                emote_packet = await Emote_k(int(uid), emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                await asyncio.sleep(0.1)
            except Exception:
                pass
        cycles += 1
        await asyncio.sleep(1)
    return cycles


# ═══════════════════════════════════════════════════════════════
# API CALLS & HELPERS
# ═══════════════════════════════════════════════════════════════

async def send_friend_request(target_uid, token, region):
    try:
        url = f"https://friend-request-api-omega.vercel.app/add_friend?token={token}&target_uid={target_uid}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False, timeout=15) as r:
                res_text = await r.text()
                
                if r.status == 200:
                    return (True, "Friend request sent successfully!")
                else:
                    return (False, f"API Error: Status {r.status} | {res_text[:60]}")
    except Exception as e:
        return False, f"System Error: {str(e)}"


async def remove_friend(target_uid, token, region):
    try:
        url = f"https://friend-request-api-omega.vercel.app/remove_friend?token={token}&target_uid={target_uid}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False, timeout=15) as r:
                res_text = await r.text()
                
                if r.status == 200:
                    return (True, "Friend removed successfully!")
                else:
                    return (False, f"API Error: Status {r.status} | {res_text[:60]}")
    except Exception as e:
        return False, f"System Error: {str(e)}"


async def join_guild(guild_id, uid, password):
    try:
        # API URL
        url = f"https://guild-join-api.vercel.app/join?guild_id={guild_id}&uid={uid}&password={password}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Accept": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, ssl=False) as r:
                try:
                    res_json = await r.json()
                except Exception:
                    res_json = {}
                
                # API থেকে আসা আসল মেসেজ এবং এরর বের করা
                api_message = res_json.get("message", "")
                raw_response = res_json.get("raw_response", {})
                raw_text = raw_response.get("raw_text", "")
                
                # যদি ২০০ আসে এবং ভেতরে কোনো এরর না থাকে
                if r.status == 200 and raw_text == "":
                    return (True, f"✓ Success! {api_message}")
                
                # যদি গেমের ভেতরের এরর থাকে (যেমন: অলরেডি ইন ক্ল্যান)
                elif raw_text:
                    if "ALREADY_IN_OTHER_CLAN" in raw_text:
                        return (False, "Failed: আপনি ইতিমধ্যে অন্য গিল্ডে আছেন! আগে গিল্ড থেকে লিভ নেন প্লিজ।")
                    else:
                        return (False, f"Failed: {raw_text}")
                
                # যদি সরাসরি স্ট্যাটাস এরর আসে
                else:
                    return (False, f" API Error: Status {r.status}")
                    
    except asyncio.TimeoutError:
        return (False, "⏳ Timeout: সার্ভার রেসপন্স করছে না।")
    except Exception as e:
        return (False, f" System Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# ❤️ LIKE SYSTEM — Manual only (No auto retry, No saving)
# ═══════════════════════════════════════════════════════════════

def _bd_now():
    """Bangladesh current time (UTC+6)"""
    return datetime.utcnow() + timedelta(hours=6)


def _seconds_until_4am():
    """Seconds left until next 4:00 AM (Bangladesh Time)"""
    now_bd = _bd_now()
    today_4am_bd = now_bd.replace(hour=4, minute=0, second=0, microsecond=0)
    if now_bd >= today_4am_bd:
        today_4am_bd += timedelta(days=1)
    utc_4am = today_4am_bd - timedelta(hours=6)
    target_epoch = (utc_4am - datetime(1970, 1, 1)).total_seconds()
    return max(0, int(target_epoch - time.time()))


def _format_duration(seconds):
    """Format seconds → '12h 10m 30s'"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = []
    if h > 0:
        parts.append(f"{h}h")
    if m > 0:
        parts.append(f"{m}m")
    if s > 0 or not parts:
        parts.append(f"{s}s")
    return " ".join(parts)


async def _call_like_api(uid):
    """Call Like API"""
    try:
        url = f"{LIKE_API_URL}?uid={uid}&server_name=bd&key={LIKE_API_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, ssl=False,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as r:
                if r.status != 200:
                    return None, f"HTTP {r.status}"
                try:
                    return await r.json(), None
                except Exception:
                    return None, "Invalid JSON"
    except asyncio.TimeoutError:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)[:80]


async def run_like_system(uid, chat_type, chat_id, key, iv, sender_uid):
    """
    Manual like flow — NO SAVING, NO AUTO RETRY.
    Sends the message in parts to prevent Free Fire from dropping it.
    """
    # 1. Processing msg
    await safe_send_message(
        chat_type,
        f"[B][C][FFFF00]⏳ Processing like...\n"
        f"[C][FFFFFF]🆔 UID: [FFFF00]{xMsGFixinG(uid)}",
        sender_uid, chat_id, key, iv
    )

    # 2. Call API
    data, err = await _call_like_api(uid)

    if err or not data:
        await safe_send_message(
            chat_type,
            f"[B][C][FF0000]❌ Like API Error\n"
            f"[C][FFFFFF]🆔 UID: [FFFF00]{xMsGFixinG(uid)}\n"
            f"[C][FFFFFF]Reason: {err}",
            sender_uid, chat_id, key, iv
        )
        return

    status = data.get("status", 0)
    print(f"❤️ [LIKE] uid={uid} → status={status}")

    # ═══ Common Data from API ═══
    nickname = data.get("PlayerNickname", "Unknown")
    level = data.get("Level", "N/A")
    server = data.get("Server", "BD")
    running_time = data.get("RunningTime", _bd_now().strftime("%I:%M %p"))
    
    before = data.get("LikesbeforeCommand", 0)
    after = data.get("LikesafterCommand", 0)
    given = data.get("LikesGivenByAPI", 0)

    # ═══ status = 1 : Success (Split into 2 parts) ═══
    if status == 1:
        # Part 1: Header & Player Info
        part1_1 = (
            f"[B][C][00FF00]╔═══════════════╗\n"
            f"[B][C][FF69B4] 🎉  LIKES SENT SUCCESSFULLY\n"
            f"[B][C][00FF00]╠═══════════════╣\n"
            f"[C][FFFFFF] 👤  Nickname » [00FF00]{nickname}\n"
            f"[C][FFFFFF] 🆔  UID      » [FFFF00]{xMsGFixinG(uid)}\n"
            f"[C][FFFFFF] 🎚️  Level    » [FF69B4]{level}\n"
            f"[C][FFFFFF] 🌍  Region   » [FF69B4]{server}"
        )
        await safe_send_message(chat_type, part1_1, sender_uid, chat_id, key, iv)

        # ৫ মিলিসেকেন্ড অপেক্ষা করার জন্য (0.005 সেকেন্ড)
        await asyncio.sleep(2.0)

        # Part 2: Likes Stats & Footer
        part1_2 = (
            f"[C][00FFFF]───────────────\n"
            f"[C][FFFFFF] 🕓  Old Likes » [FF8888]{before}\n"
            f"[C][FFFFFF] 📈  Total Likes » [FFFF00]{after}\n"
            f"[C][FFFFFF] ✨ add Likes » [00FF00]+{given}\n"
            f"[C][00FFFF]───────────────\n"
            f"[C][00FF00]      Use Only One\n"
            f"[C][FFFFFF]      Status : [00FF00]1\n"
            f"[B][C][00FF00]╚═══════════════╝\n"
            f"[C][FF00FF]⚡ YASIN × BHAI Bot"
        )
        await safe_send_message(chat_type, part1_2, sender_uid, chat_id, key, iv)

    # ═══ status = 2 : Already Liked (Split into 2 parts) ═══
    elif status == 2:
        remaining_sec = _seconds_until_4am()
        time_text = _format_duration(remaining_sec)

        # Part 1: Header & Player Info
        part2_1 = (
            f"[B][C][FFA500]╔═══════════════╗\n"
            f"[B][C][FFA500]   ⏳ ALREADY LIKED\n"
            f"[B][C][FFA500]╠═══════════════╣\n"
            f"[C][FFFFFF] 👤  Nickname » [00FF00]{nickname}\n"
            f"[C][FFFFFF] 🆔  UID      » [FFFF00]{xMsGFixinG(uid)}\n"
            f"[C][FFFFFF] 🎚️  Level    » [FF69B4]{level}\n"
            f"[C][FFFFFF] 🌍  Region   » [FF69B4]{server}"
        )
        await safe_send_message(chat_type, part2_1, sender_uid, chat_id, key, iv)

        # Part 2: Timer & Footer
        part2_2 = (
            f"[C][00FFFF]───────────────\n"
            f"[C][FFFFFF] 📝 Already received likes\n"
            f"[C][00FFFF]───────────────\n"
            f"[C][FFFFFF] 🌅 Reset Time » [00FFFF]4:00 AM (BD)\n"
            f"[C][FFFFFF]  Remaining  » [FFA500]{time_text}\n"
            f"[C][FFFFFF]  Running Time » [FFA500]{running_time}\n"
            f"[B][C][FFA500]╚═══════════════╝\n"
            f"[C][FF00FF]⚡ YASIN × BHAI Bot"
        )
        await safe_send_message(chat_type, part2_2, sender_uid, chat_id, key, iv)

    # ═══ Unknown status ═══
    else:
        await safe_send_message(
            chat_type,
            f"[B][C][FFA500]⚠️ Unknown status» {status}\n"
            f"[C][FFFFFF]🆔 UID» [FFFF00]{xMsGFixinG(uid)}",
            sender_uid, chat_id, key, iv
        )

async def get_player_info(player_id):
    try:
        url = f"https://nirob-x-info.vercel.app/info?uid={player_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200: return True, await r.json()
                return False, f"HTTP {r.status}"
    except Exception as e: return False, str(e)


def format_player_info(data):
    if data.get("status") != "success" and "basicInfo" not in data:
        return [f"[B][C][FF0000]✗ API Error: {data.get('message', 'Unknown')}"]
    
    b = data.get("basicInfo", {})
    g = data.get("clanBasicInfo", {})
    l = data.get("captainBasicInfo", {})
    p = data.get("petInfo", {})
    s = data.get("socialInfo", {})
    c = data.get("creditScoreInfo", {})
    ban = data.get("banStatus", "Normal")

    p1 = f"""[B]{get_random_color()} ═══1 PLAYER INFO ═══
[B][C][FFFFFF]Name» [00FF00]{b.get('nickname', 'N/A')}
[B][C][FFFFFF]UID» [FFFF00]{b.get('accountId', 'N/A')}
[B][C][FFFFFF]Region» [FF69B4]{b.get('region', 'N/A')}
[B][C][FFFFFF]Level» [FFA500]{b.get('level', 'N/A')}
[B][C][FFFFFF]Likes» [FF1493]{b.get('liked', 'N/A')}
[B][C][FFFFFF]BR Rank» [00FFFF]{b.get('rank', 'N/A')} ({b.get('rankingPoints', 0)} pts)
[B][C][FFFFFF]Ban Status» {ban}
[B][C][FFFFFF]Bio» [D3D3D3]{s.get('signature', 'N/A')}
[B]{get_random_color()} ══════════════════"""

    p2 = f"""[B]{get_random_color()} ═══2 GUILD & LEADER ═══
[B][C][FFFFFF]Guild Name» [00FF7F]{g.get('clanName', 'No Guild')}
[B][C][FFFFFF]Guild ID» [FFFF00]{g.get('clanId', '0')}
[B][C][FFFFFF]Guild Level» [FFA500]{g.get('clanLevel', '0')}
[B][C][FFFFFF]Members» [FF69B4]{g.get('memberNum', 0)}/{g.get('capacity', 0)}
[B][C][FFFFFF]Leader Name» [00FFFF]{l.get('nickname', 'N/A')}
[B][C][FFFFFF]Leader UID» [FFFF00]{l.get('accountId', 'N/A')}
[B][C][FFFFFF]Leader Lvl» [FFA500]{l.get('level', 'N/A')}
[B][C][FFFFFF]Leader BR» [00FF00]{l.get('rank', 'N/A')}
[B]{get_random_color()} ═════════════════"""

    p3 = f"""[B]{get_random_color()} ═══3 ACTIVITY & EXTRA ═══
[B][C][FFFFFF]Pet» [FF69B4]{p.get('petNick', 'N/A')} (Lv {p.get('petLevel', 0)})
[B][C][FFFFFF]Honor Score» [00FF00]{c.get('creditScore', 0)}
[B][C][FFFFFF]Created» [D3D3D3]{b.get('createdAt', 'N/A')}
[B][C][FFFFFF]Last Login» [D3D3D3]{b.get('lastLoginAt', 'N/A')}
[B][C][FFFFFF]CS Rank» [00FFFF]{b.get('csRank', 'N/A')}

[B]{get_random_color()} ✨ Powered by » YASIN × BHAI"""
    return [p1, p2, p3]


def format_check_result(data):
    try: return f"[b]{get_random_color()} 🔍 BAN CHECK\n[b][c][FFFFFF]Type: {data.get('ban_type', 'Unknown')}\n[b][c][FFFFFF]Duration: {data.get('ban_duration', 'Unknown')}"
    except Exception as e: return f"[b][c]Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# STATUS, MIMIC, /Equip hi emote, /ban check HELPERS
# ═══════════════════════════════════════════════════════════════

async def createpacketinfo(uid, key, iv):
    try:
        ida = await EnC_Uid(str(uid), Tp='Uid')
        if isinstance(ida, bytes):
            ida = ida.hex()
        
        if len(ida) == 16: 
            packet = f'080112080a04{ida}1005'
        elif len(ida) == 20: 
            packet = f"080112090a05{ida}1005"
        else:
            packet = f"080112090A05{ida}1005"
            
        return await GeneRaTePk(packet, '0f15', key, iv)
    except Exception as e:
        log_error_to_file(str(e), context="createpacketinfo")
        return None


def get_available_room(hex_packet):
    try:
        res = PrOtO(hex_packet)
        if isinstance(res, dict):
            return json.dumps(res)
        return str(res)
    except Exception as e:
        log_error_to_file(str(e), context="get_available_room")
        return None


def get_player_status(packet):
    j = get_available_room(packet)
    if not j:
        return "OFFLINE"
    try:
        p = json.loads(j)
        if not isinstance(p, dict):
            return "OFFLINE"
            
        f5 = p.get("5", {})
        f5_data = f5.get("data", f5) if isinstance(f5, dict) else f5
        if isinstance(f5_data, dict):
            f1 = f5_data.get("1", {})
            f1_data = f1.get("data", f1) if isinstance(f1, dict) else f1
            if not isinstance(f1_data, dict):
                f1_data = f5_data
        else:
            f1_data = {}

        if not isinstance(f1_data, dict):
            return "OFFLINE"
            
        st_field = f1_data.get("3", {})
        st = st_field.get("data", st_field) if isinstance(st_field, dict) else st_field
        if isinstance(st, dict):
            st = st.get("data", 0)
            
        if st == 1:
            return "SOLO"
        if st == 2:
            nine = f1_data.get("9", {})
            nine_data = nine.get("data", nine) if isinstance(nine, dict) else nine
            if isinstance(nine_data, dict):
                gc_field = nine_data.get("data", nine_data.get("1"))
                gc = gc_field.get("data", gc_field) if isinstance(gc_field, dict) else gc_field
            else:
                gc = nine_data
                
            ten = f1_data.get("10", {})
            ten_data = ten.get("data", ten) if isinstance(ten, dict) else ten
            if isinstance(ten_data, (int, float)):
                mx = int(ten_data) + 1
                if gc is not None:
                    return f"INSQUAD ({gc}/{mx})"
            return "INSQUAD"
        if st in (3, 5):
            return "INGAME"
        if st == 4:
            return "IN ROOM"
        if st in (6, 7):
            return "IN SOCIAL ISLAND MODE"
        return "NOTFOUND"
    except Exception as e:
        log_error_to_file(str(e), context="get_player_status")
        return "OFFLINE"


def get_idroom_by_idplayer(packet):
    try:
        p = json.loads(get_available_room(packet))
        if not isinstance(p, dict):
            return None
        f5 = p.get("5", {})
        f5_data = f5.get("data", f5) if isinstance(f5, dict) else f5
        if isinstance(f5_data, dict):
            f1 = f5_data.get("1", {})
            f1_data = f1.get("data", f1) if isinstance(f1, dict) else f1
            if isinstance(f1_data, dict):
                room = f1_data.get("15", {})
                return room.get("data", room) if isinstance(room, dict) else room
    except Exception as e:
        log_error_to_file(str(e), context="get_idroom_by_idplayer")
        return None
    return None


def get_leader(packet):
    try:
        p = json.loads(get_available_room(packet))
        if not isinstance(p, dict):
            return None
        f5 = p.get("5", {})
        f5_data = f5.get("data", f5) if isinstance(f5, dict) else f5
        if isinstance(f5_data, dict):
            f1 = f5_data.get("1", {})
            f1_data = f1.get("data", f1) if isinstance(f1, dict) else f1
            if isinstance(f1_data, dict):
                leader = f1_data.get("8", {})
                return leader.get("data", leader) if isinstance(leader, dict) else leader
    except Exception as e:
        log_error_to_file(str(e), context="get_leader")
        return None
    return None


def save_to_cache(player_id, data):
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "rb") as f:
                cache = pickle.load(f)
        except Exception:
            cache = {}
    data["saved_at"] = time.time()
    cache[str(player_id)] = data
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)


def load_from_cache(player_id):
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
    except Exception:
        return None
    key = str(player_id)
    if key in cache:
        if time.time() - cache[key].get("saved_at", 0) > CACHE_TIMEOUT:
            del cache[key]
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(cache, f)
            return None
        return cache[key]
    return None


def clear_cache_entry(player_id):
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "rb") as f:
                cache = pickle.load(f)
            cache.pop(str(player_id), None)
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(cache, f)
        except Exception:
            pass


def debug_file_cache():
    if not os.path.exists(CACHE_FILE):
        print("Cache: file does not exist")
        return
    try:
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        print(f"Cache: {len(cache)} entries")
        for k, v in cache.items():
            age = time.time() - v.get("saved_at", 0)
            print(f"  {k}: {v.get('status','?')} (age {age:.1f}s)")
    except Exception as e:
        print(f"Cache debug error: {e}")


async def extract_emote_info(data_hex, key, iv):
    try:
        packet_json = json.loads(await DeCode_PackEt(data_hex[10:]))
    except Exception:
        return None
    for extractor in (extract_type_21, extract_type_26,
                      extract_type_5, generic_extract):
        info = extractor(packet_json)
        if info and info.get("sender_uid"):
            return info
    return None


def extract_type_21(packet_json):
    if packet_json.get("1") == 21:
        try:
            nested = packet_json["2"]["data"]["5"]["data"]
            sender = nested.get("1", {}).get("data")
            emote  = nested.get("3", {}).get("data")
            if sender and emote:
                return {"sender_uid": sender, "emote_id": emote,
                        "packet_type": 21, "confidence": "high"}
        except Exception:
            pass
    return None


def extract_type_26(packet_json):
    if packet_json.get("1") == 26:
        try:
            data   = packet_json["2"]["data"]
            sender = data.get("1", {}).get("data")
            emote  = data.get("2", {}).get("data")
            if sender and emote:
                return {"sender_uid": sender, "emote_id": emote,
                        "packet_type": 26, "confidence": "high"}
        except Exception:
            pass
    return None


def extract_type_5(packet_json):
    if packet_json.get("1") == 5:
        try:
            data   = packet_json["2"]["data"]
            sender = data.get("1", {}).get("data")
            emote  = data.get("4", {}).get("data") or 909051015
            if sender:
                return {"sender_uid": sender, "emote_id": emote,
                        "packet_type": 5, "confidence": "medium"}
        except Exception:
            pass
    return None


def generic_extract(packet_json):
    uid, emote_id = None, None

    def search(obj):
        nonlocal uid, emote_id
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "data" and isinstance(v, (int, str)) and str(v).isdigit():
                    num = int(v)
                    if 1_000_000 < num < 99_999_999_999 and not uid:
                        uid = num
                    elif str(v).startswith("909") and len(str(v)) >= 9:
                        emote_id = num
                elif isinstance(v, dict):
                    search(v)
                elif isinstance(v, list):
                    for item in v:
                        search(item)

    search(packet_json)
    if uid:
        return {"sender_uid": uid,
                "emote_id":   emote_id or 909051015,
                "packet_type": "generic", "confidence": "medium"}
    return None

async def do_squad_refresh(key, iv, chat_type, chat_id, sender_uid):
    global current_squad_code, online_writer, bot_uid

    if not current_squad_code or str(current_squad_code) in ("None", "", "0", "1"):
        print(f"⚠️ [SQUAD REFRESH] Invalid/no squad code ({current_squad_code}) — skipping")
        return

    saved_code = str(current_squad_code).strip()
    print(f"🔄 [SQUAD REFRESH] Starting: exit → rejoin using /join system with code {saved_code}")

    # ---- STEP 1: EXIT ----
    try:
        try:
            result = ExitSq(int(bot_uid), key, iv)
            if asyncio.iscoroutine(result):
                exit_packet = await result
            else:
                exit_packet = result
        except Exception:
            leave_fields = {1: 1, 2: {1: int(bot_uid), 2: 1, 3: "en"}}
            exit_packet = await GeneRaTePk((await CrEaTe_ProTo(leave_fields)).hex(), '0515', key, iv)

        if exit_packet and online_writer:
            if isinstance(exit_packet, str):
                exit_packet = bytes.fromhex(exit_packet)
            online_writer.write(exit_packet)
            await online_writer.drain()
            print("🚪 [SQUAD REFRESH] Exit packet sent successfully")
    except Exception as ex:
        print(f"✗ Exit error: {ex}")

    # গ্যারেনাকে লিভ প্রসেস করতে ৩ সেকেন্ড সময় দাও
    await asyncio.sleep(3.0)

    # ---- STEP 2: REJOIN ----
    try:
        # যেহেতু আমরা সরাসরি ৭ ডিজিটের কোড সেভ করছি, তাই সরাসরি JoinSq_original কল করবো
        rejoin_packet = await JoinSq_original(saved_code, key, iv)
        
        if rejoin_packet and online_writer:
            online_writer.write(rejoin_packet)
            await online_writer.drain()
            print(f"🔄 [SQUAD REFRESH] Rejoin packet sent for {saved_code}")
            
            await safe_send_message(
                chat_type,
                f"[B][C][00FF00]✓ Bot auto-rejoined the squad!",
                sender_uid, chat_id, key, iv
            )
    except Exception as ex:
        print(f"✗ Rejoin error: {ex}")


async def equip_hi_emote(sender_uid, chat_id, chat_type, key, iv, region_default="BD"):
    def fmt_num(n):
        return str(n)

    if str(sender_uid) != str(admin_uid):
        try:
            await safe_send_message(chat_type, "Only admin use.", sender_uid, chat_id, key, iv)
        except Exception as e:
            log_error_to_file(str(e), context="equip_hi_emote - Admin Check")
        return

    global ToKen, region, bot_uid, current_squad_code
    active_token = ToKen
    if not active_token:
        err_msg = "Error: Bot active token not found."
        log_error_to_file(err_msg, context="equip_hi_emote - Token Check")
        try:
            await safe_send_message(chat_type, f"[B][C][FF0000]{err_msg}", sender_uid, chat_id, key, iv)
        except Exception:
            pass
        return

    try:
        # ১. প্রসেসিং মেসেজ
        try:
            await safe_send_message(
                chat_type,
                "[B][C][FFFF00]Equipping HI emote, please wait...",
                sender_uid, chat_id, key, iv
            )
        except Exception as e:
            log_error_to_file(str(e), context="equip_hi_emote - Initial Message")

        await asyncio.sleep(0.5)

        current_region = region if region else region_default
        region_server_map = {
            "BD":  "https://clientbp.ppmainecoonghj.com",
            "IND": "https://client.ind.freefiremobile.com",
            "PK":  "https://clientbp.ggpolarbear.com",
            "ME":  "https://clientbp.ggpolarbear.com",
            "VN":  "https://clientbp.ggpolarbear.com",
            "SG":  "https://clientbp.ggpolarbear.com",
            "ID":  "https://clientbp.ggpolarbear.com",
            "TH":  "https://clientbp.ggpolarbear.com",
            "BR":  "https://client.us.freefiremobile.com",
            "NA":  "https://client.us.freefiremobile.com",
            "US":  "https://client.us.freefiremobile.com",
            "RU":  "https://clientbp.ggpolarbear.com",
        }
        server_url = region_server_map.get(str(current_region).upper(), "https://clientbp.ggpolarbear.com")

        emote_data = bytes.fromhex("CAF683222A25C7BEFEB51F59544DB313")
        headers = {
            "Accept-Encoding": "gzip",
            "Connection":      "Keep-Alive",
            "Content-Type":    "application/x-www-form-urlencoded",
            "Expect":          "100-continue",
            "ReleaseVersion":  "OB55",
            "User-Agent":      "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "X-GA":            "v1 1",
            "X-Unity-Version": "2018.4.11f1",
            "Authorization":   f"Bearer {active_token}",
        }
        url = f"{server_url}/ChooseEmote"

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, data=emote_data, ssl=False) as resp:
                status_code   = resp.status
                response_body = await resp.read()

        # ২. রেজাল্ট মেসেজ
        if status_code == 200:
            result_msg = "[B][C][00FF00]✓ SUCCESS: HI Emote Equipped"
        elif b"BR_INVENTORY_NOT_ENOUGH_ITEMS" in response_body:
            result_msg = "[B][C][FF0000]✗ FAILED: Emote Not Owned"
        else:
            result_msg = f"[B][C][FF0000]✗ FAILED: Status {status_code}"
            log_error_to_file(f"ChooseEmote API failed with status {status_code}, body: {response_body}", context="equip_hi_emote - API Response")

        await asyncio.sleep(0.3)
        try:
            await safe_send_message(chat_type, result_msg, sender_uid, chat_id, key, iv)
        except Exception as e:
            log_error_to_file(str(e), context="equip_hi_emote - Result Message")

        # ৩. শুধু সফল হলে → exit → rejoin (kick হলে এটা হবে না)
        if status_code == 200:
            await asyncio.sleep(1.0)
            await do_squad_refresh(key, iv, chat_type, chat_id, sender_uid)

    except Exception as e:
        log_error_to_file(str(e), context="equip_hi_emote - Main Try Block")
        err_msg = f"[B][C][FF0000]✗ FAILED: System Error ({str(e)[:40]})"
        try:
            await safe_send_message(chat_type, err_msg, sender_uid, chat_id, key, iv)
        except Exception as inner_e:
            log_error_to_file(str(inner_e), context="equip_hi_emote - Error Message Send Failure")


async def check_ban_auto(uid):
    name, region_code = "N/A", "N/A"
    is_banned_str = "Not Banned"
    try:
        ok, data = await get_player_info(uid)
        if ok and isinstance(data, dict):
            b = data.get("BasicInformation", {}) or {}
            name = b.get("Name", "N/A")
            region_code = b.get("Region", "N/A")
            is_banned_str = data.get("BanStatus", "Not Banned")
    except Exception as e:
        print(f"Check ban error: {e}")

    is_banned = 1 if "banned" in str(is_banned_str).lower() or str(is_banned_str) == "1" else 0
    status_text  = "BANNED"     if is_banned == 1 else "NOT BANNED"
    status_color = "FF0000"     if is_banned == 1 else "00FF00"
    
    period_text  = str(is_banned_str) if is_banned == 1 else "N/A"
    period_color = "FF4444"           if is_banned == 1 else "00FF00"

    return (
        f"[C][B][5DA9FF]━━━━━━━━━━━━━\n"
        f"[C][B][FF6EC7]BAN STATUS CHECK\n"
        f"[C][5DA9FF]━━━━━━━━━━━━━\n"
        f"[C][E6E6FA]Name  » [9AD0FF]{name}\n"
        f"[C][E6E6FA]UID      » [9AD0FF]{xMsGFixinG(uid)}\n"
        f"[C][E6E6FA]Region » [9AD0FF]{region_code}\n"
        f"[C][E6E6FA]Status  » [{status_color}]{status_text}\n"
        f"[C][E6E6FA]Period  » [{period_color}]{period_text}\n"
        f"[C][B][5DA9FF]━━━━━━━━━━━━━"
    )


# ═══════════════════════════════════════════════════════════════
# ONLINE TCP HANDLER (WITH AUTO-RECONNECT & STATE RESET)
# ═══════════════════════════════════════════════════════════════

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=1.0):
    global online_writer, whisper_writer, region
    global pending_ghost_future, ghost_team_id, ghost_squad_code
    global emote_hijack, bot_uid, current_squad_code, bot_in_squad

    if not bot_uid:
        bot_uid = extract_bot_uid_from_auth(AutHToKen)

    fail_count = 0
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            fail_count = 0  # সফল কানেকশন হলে কাউন্টার রিসেট হবে
            token_bytes = bytes.fromhex(AutHToKen) if isinstance(AutHToKen, str) else AutHToKen
            writer.write(token_bytes)
            await writer.drain()
            print(f"✓ ONLINE connected to {ip}:{port}")

            while True:
                data = await reader.read(9999)
                if not data:
                    break
                hex_data = data.hex()

                if hex_data.startswith("0f00") and len(hex_data) > 100:
                    try:
                        print("📡 Received status response packet")
                        proto_hex = hex_data[10:] 
                        parsed = get_available_room(proto_hex)
                        if parsed:
                            pj = json.loads(parsed)
                            if isinstance(pj, dict):
                                f2 = pj.get("2", {})
                                f2_data = f2.get("data") if isinstance(f2, dict) else f2
                                if f2_data == 15 or True:
                                    f5 = pj.get("5", {})
                                    f5_data = f5.get("data", f5) if isinstance(f5, dict) else f5
                                    
                                    player_id = None
                                    f1_data = {}
                                    if isinstance(f5_data, dict):
                                        f1 = f5_data.get("1", {})
                                        f1_data = f1.get("data", f1) if isinstance(f1, dict) else f1
                                        if isinstance(f1_data, dict):
                                            id_field = f1_data.get("1", {})
                                            player_id = id_field.get("data", id_field) if isinstance(id_field, dict) else id_field
                                            if not player_id:
                                                player_id = f1_data.get("accountId", f1_data.get("uid"))
                                        elif isinstance(f1_data, (int, str)):
                                            player_id = f1_data
                                            
                                        if not player_id:
                                            d_field = f5_data.get("data", f5_data.get("accountId", f5_data.get("uid")))
                                            if isinstance(d_field, dict):
                                                player_id = d_field.get("data", d_field)
                                            else:
                                                player_id = d_field

                                    player_status = get_player_status(proto_hex)
                                    
                                    entry = {
                                        "status":      player_status,
                                        "packet":      proto_hex,
                                        "timestamp":   time.time(),
                                        "full_packet": hex_data,
                                        "parsed_json": pj,
                                    }
                                    
                                    d1 = f1_data if isinstance(f1_data, dict) else (f5_data if isinstance(f5_data, dict) else {})
                                    if isinstance(d1, dict):
                                        s3 = d1.get("3", {})
                                        s11 = d1.get("11", {})
                                        val3 = s3.get("data", s3) if isinstance(s3, dict) else s3
                                        val11 = s11.get("data", s11) if isinstance(s11, dict) else s11
                                        if val3 == 1 and val11 == 1:
                                            entry["special_state"] = "SOLO_WITH_FLAG_1"
                                    
                                    if "IN ROOM" in player_status:
                                        rid = get_idroom_by_idplayer(proto_hex)
                                        if rid:
                                            entry["room_id"] = rid
                                    elif "INSQUAD" in player_status:
                                        lid = get_leader(proto_hex)
                                        if lid:
                                            entry["leader_id"] = lid
                                            
                                    if player_id:
                                        save_to_cache(str(player_id), entry)
                                        print(f"✓ Cached status: {player_id} = {player_status}")
                    except Exception as e:
                        log_error_to_file(str(e), context="TcPOnLine Status Handler")
                        print(f"✗ status parse error: {e}")
                    continue

                if hex_data.startswith('05') and len(hex_data) > 20 and emote_hijack:
                    try:
                        import re
                        payload = hex_data[10:]
                        packet_str = await DeCode_PackEt(payload)
                        if not packet_str or '9090' not in packet_str:
                            try:
                                decrypted = await DEc_PacKeT(payload, key, iv)
                                packet_str = await DeCode_PackEt(decrypted)
                            except Exception:
                                pass

                        if packet_str and '9090' in packet_str:
                            emote_match = re.search(r'"data":\s*(9090\d{5})', packet_str)
                            if emote_match:
                                emote_id = emote_match.group(1)
                                all_ids = re.findall(r'"data":\s*(\d{8,12})', packet_str)
                                sender_uid = None
                                for u in all_ids:
                                    if str(u) != str(bot_uid) and not str(u).startswith('9090'):
                                        sender_uid = u
                                        break

                                if emote_id and sender_uid and str(sender_uid) != str(bot_uid):
                                    bot_self_emote = await Emote_k(int(bot_uid), int(emote_id), key, iv, region)
                                    if online_writer:
                                        online_writer.write(bot_self_emote)
                                        await online_writer.drain()
                                    print(f"\n🎯 MIMIC SUCCESS!\n   👤 From: {sender_uid}\n   🎭 Emote: {emote_id}")
                    except Exception as e:
                        log_error_to_file(str(e), context="Mimic Handler")
                        print(f"✗ Mimic error: {e}")

                if not hex_data.startswith("0500"):
                    continue

                try:
                    packet_json = json.loads(await DeCode_PackEt(hex_data[10:]))
                except Exception:
                    continue

                try:
                    if ('5' in packet_json and 'data' in packet_json['5'] and
                            '1' in packet_json['5']['data'] and '8' in packet_json['5']['data']):
                        owner = packet_json['5']['data']['1']['data']
                        raw_code = packet_json['5']['data']['8']['data']
                        
                        code_str = str(raw_code).strip()
                        if code_str and len(code_str) > 10 and "_" in code_str:
                            current_squad_code = code_str
                            bot_in_squad = True
                            print(f"📩 Squad invite from {owner}")
                            print(f"💾 Saved squad code: {current_squad_code}")
                        else:
                            code_str = None
                        
                        if code_str:
                            join_pkt = await YASIN_BHAI_Accepted(owner, code_str, key, iv, region)
                            if join_pkt and online_writer:
                                online_writer.write(join_pkt)
                                await online_writer.drain()
                                print(f"✓ Accepted squad invite from {owner} and joined!")
                                
                                # নতুন ফিচার: ম্যানুয়ালি ইনভাইট দিলে বটের পক্ষ থেকে ব্যাক ইনভাইট পাঠানো
                                try:
                                    await asyncio.sleep(0.6)
                                    back_invite_pkt = await SPamSqForSpm(int(owner), key, iv)
                                    if back_invite_pkt and online_writer:
                                        online_writer.write(back_invite_pkt)
                                        await online_writer.drain()
                                        print(f"📩 Manual invite back sent to {owner}")
                                except Exception as be:
                                    print(f"Manual invite back error: {be}")
                            else:
                                print("⚠️ Join packet None or writer inactive")
                except Exception as e:
                    print(f"✗ Invite accept error: {e}")

                try:
                    uid_g, chat_code, squad_code = await GeTSQDaTa(packet_json)
                    if uid_g is not None:
                        # প্রতিবার ইনভাইট দিলে বা কিক খাওয়ার পর রি-ইনভাইট দিলে কোড যেন গ্লিচ না করে এবং ওয়েলকাম মেসেজ বাধ্যতামূলক দেখায়
                        WELCOMED.pop(chat_code, None)
                        
                        INV_JOIN = await AutH_Chat(3, uid_g, chat_code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', INV_JOIN)
                        asyncio.create_task(send_welcome(uid_g, key, iv))

                        # ২য় ও ৩য় কাজ: ওয়েলকাম মেসেজ শো হওয়ার পর ইমোট এবং বান্ডেল/পিন সিস্টেম ১০০% কাজ করবে
                        try:
                            await asyncio.sleep(0.8)
                            random_emote = random.choice([909000085, 909000063])
                            emote_pkt = await Emote_k(int(uid_g), int(random_emote), key, iv, region)
                            if emote_pkt and online_writer:
                                online_writer.write(emote_pkt)
                                await online_writer.drain()
                                print(f"🎭 Auto Invite Emote Sent: {random_emote} to {uid_g}")
                        except Exception as e:
                            print(f"Auto Invite Emote Error: {e}")

                        try:
                            await asyncio.sleep(0.5)
                            random_bundle = random.choice([914000002, 914039001, 914042001, 914053001])
                            
                            anim_pkt = await animation_packet(random_bundle, key, iv)
                            if anim_pkt and online_writer:
                                online_writer.write(anim_pkt)
                                await online_writer.drain()
                            
                            await asyncio.sleep(0.5)
                            
                            bundle_pkt = await Look_Changer(random_bundle, key, iv, look_type=1, region=region)
                            if bundle_pkt and online_writer:
                                online_writer.write(bundle_pkt)
                                await online_writer.drain()
                                print(f"✓ Random Bundle {random_bundle} equipped successfully on Bot")
                        except Exception as e:
                            print(f"Bot Bundle Error: {e}")

                        try:
                            p1 = await DEVIL1(uid_g, key, iv)
                            p2 = await DEVIL(uid_g, key, iv)
                            if p1 and online_writer:
                                online_writer.write(p1)
                                await online_writer.drain()
                                await asyncio.sleep(0.2)
                            if p2 and online_writer:
                                online_writer.write(p2)
                                await online_writer.drain()
                        except Exception:
                            pass
                except Exception:
                    pass

                try:
                    if pending_ghost_future and not pending_ghost_future.done():
                        f5 = packet_json.get('5', {}).get('data', {})
                        if '31' in f5:
                            ghost_squad_code = f5['31'].get('data')
                        if '1' in f5:
                            ghost_team_id = f5['1'].get('data')
                        if ghost_team_id and ghost_squad_code:
                            pending_ghost_future.set_result(True)
                except Exception:
                    pass

                try:
                    if packet_json.get('4', {}).get('data') == 8:
                        f5 = packet_json.get('5', {}).get('data', {})
                        if f5.get('2', {}).get('data') == 5:
                            chat_code = f5.get('17', {}).get('data')
                            if chat_code is not None:
                                WELCOMED.pop(chat_code, None)
                                LeAvE = await leave_channel_req(chat_code, 3, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', LeAvE)
                                print("🚪 Kicked! Left channel -> Refreshing Bot State")
                                # ⚡ এখানে কিক খাওয়ার সাথে সাথে বট রিফ্রেশ হবে ⚡
                                await refresh_bot_state()
                except Exception:
                    pass

            writer.close()
            await writer.wait_closed()
            online_writer = None
        except Exception as e:
            fail_count += 1
            log_error_to_file(str(e), context="TcPOnLine Connection")
            print(f"Online connection error: {ip}:{port} - {e} (Fail #{fail_count}) -> Refreshing...")
            online_writer = None
            await refresh_bot_state()
            if fail_count >= 5:
                raise Exception("Online connection failed repeatedly. Forcing full re-login...")
        await asyncio.sleep(min(reconnect_delay * fail_count, 10.0))

# ═══════════════════════════════════════════════════════════════
# CHAT TCP HANDLER (WITH AUTO-RECONNECT & STATE RESET)
# ═══════════════════════════════════════════════════════════════

async def TcPChaT(ip, port, AutHToKen, key, iv, ready_event, region,
                  clan_id=None, clan_data=None, reconnect_delay=0.5):
    global whisper_writer, online_writer, spm_tasks, ToKen, bot_uid
    global bot_enabled, emote_hijack, spam_targets
    global evo_cycle_running, evo_cycle_task, ban_task, ban_running, ban_targets
    global fast_spam_running, fast_spam_task
    global custom_spam_running, custom_spam_task
    global msg_spam_running, msg_spam_task, mg_spam_task
    global reject_spam_running, reject_spam_task
    global freeze_running, freeze_task
    global room_spam_targets, room_spam_tasks
    global _clan_message_task, _clan_msg_key, _clan_msg_iv
    global _clan_msg_bot_uid, _clan_msg_clan_id, NUMBER_EMOTES
    global current_squad_code, lag_task, lag_running   # 👈 এই লাইনটি যোগ করতে হবে

    if 'NUMBER_EMOTES' not in globals() or NUMBER_EMOTES is None:
        NUMBER_EMOTES = {}
    NUMBER_EMOTES["99"] = {"id": "909000002", "name": "lol"}

    if not bot_uid:
        bot_uid = extract_bot_uid_from_auth(AutHToKen)

    print(f"📡 {region} → TCP CHAT connecting...")

    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen) if isinstance(AutHToKen, str) else AutHToKen
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            print(f"✓ CHAT connected to {ip}:{port}")

            if clan_id and clan_data:
                try:
                    pK = await AuthClan(clan_id, clan_data, key, iv)
                    whisper_writer.write(pK)
                    await whisper_writer.drain()
                    print(f"✓ AuthClan sent for clan {clan_id}")
                except Exception as e:
                    print(f"✗ AuthClan failed: {e}")
            else:
                print(f"⚠️ No clan_id/clan_data — clan chat unavailable")

            if clan_id and clan_id > 0:
                if _clan_message_task is None or _clan_message_task.done():
                    _clan_msg_key = key
                    _clan_msg_iv = iv
                    _clan_msg_bot_uid = int(bot_uid)
                    _clan_msg_clan_id = int(clan_id)
                    _clan_message_task = asyncio.create_task(clan_message_loop())
                    print(f"[CLAN] Auto-message task started for clan {_clan_msg_clan_id}")

            for tgt in spam_targets:
                if tgt not in spm_tasks or spm_tasks[tgt].done():
                    spm_tasks[tgt] = asyncio.create_task(spm_loop(tgt, key, iv))

            while True:
                data = await reader.read(9999)
                if not data:
                    break
                if not data.hex().startswith("120000"):
                    continue

                try:
                    response = await DecodeWhisperMessage(data.hex()[10:])
                    uid = response.Data.uid
                    chat_id = response.Data.Chat_ID
                    XX = response.Data.chat_type
                    inPuTMsG = response.Data.msg.lower()
                    msg_raw = response.Data.msg
                except Exception:
                    continue

                try:
                    msg_str = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg_str) if msg_str else {}

                    if "5" in chatdata and "data" in chatdata["5"]:
                        inner = chatdata["5"]["data"]

                        if "8" in inner and "data" in inner["8"]:
                            raw_data = inner["8"]["data"]
                            try:
                                data_json = json.loads(raw_data)
                                packet_type = data_json.get("type")

                                if packet_type == "Sticker":
                                    target_uid = inner["1"]["data"]
                                    if str(target_uid) != str(bot_uid) and NUMBER_EMOTES:
                                        random_emote_key = random.choice(list(NUMBER_EMOTES.keys()))
                                        raw_emote = NUMBER_EMOTES[random_emote_key]
                                        emote_id = raw_emote["id"] if isinstance(raw_emote, dict) else raw_emote
                                        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
                                        if emote_packet and online_writer:
                                            online_writer.write(emote_packet)
                                            await online_writer.drain()
                                            print(f"🎭 Sticker Reply: Emote {emote_id} sent to {target_uid}")
                                        
                                        sticker_reply = "[B][C][FFFF00] আমি আগে থেকেই জানতাম তুই গরিব!"
                                        await safe_send_message(XX, sticker_reply, target_uid, chat_id, key, iv)
                                        
                                        # সামান্য মিলিসেকেন্ড (2ms) বিরতি দিয়ে বটের নিজের ইউআইডিতে লল ইমোট (909000002) পাঠানো
                                        await asyncio.sleep(0.002)
                                        lol_emote_id = 909000002
                                        lol_packet = await Emote_k(int(bot_uid), int(lol_emote_id), key, iv, region)
                                        if lol_packet and online_writer:
                                            online_writer.write(lol_packet)
                                            await online_writer.drain()
                                            print(f"😂 Bot LOL Emote: Sent {lol_emote_id} to Bot UID {bot_uid}")

                                elif packet_type == "Title":
                                    sender_uid = inner["1"]["data"]
                                    title_id = data_json.get("TitleID")

                                    if str(sender_uid) != str(bot_uid):
                                        try:
                                            nickname = response.Data.Details.Nickname
                                        except Exception:
                                            nickname = "Player"

                                        if str(sender_uid) == str(admin_uid):
                                            reply_msg = f"[B][C][00FF00]স্বাগতম বস {nickname} ভাই!\n[FFFF00]আপনার টাইটেলটি অসাধারণ। [00FFFF]সিস্টেমের সাথে যুক্ত করা হলো!"
                                        else:
                                            reply_msg = f"[B][C][00FF00]{nickname}, এই মাদার-চো-দ!\n[FFFF00]তুই আমার টাইটেল চুরি করেছ,\n[00FFFF]তোর মা-কে-চো-দি তোর এই টাইটেল এখন YASIN × BHAI ☆ এর!"

                                        await safe_send_message(XX, reply_msg, sender_uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                                        title_packet = await convert_kyro_to_your_system(
                                            target_uid=sender_uid,
                                            chat_id=chat_id,
                                            key=key,
                                            iv=iv,
                                            nickname="YASIN × BHAI",
                                            title_id=title_id
                                        )
                                        if title_packet and whisper_writer:
                                            whisper_writer.write(title_packet)
                                            await whisper_writer.drain()
                                            print(f"✓ Title {title_id} copied from {sender_uid}")

                                        if NUMBER_EMOTES:
                                            emote_id = "909000002"
                                            target_uids_to_emote = []
                                            if str(sender_uid) == str(admin_uid):
                                                target_uids_to_emote.append(int(admin_uid))
                                                target_uids_to_emote.append(int(bot_uid))
                                            else:
                                                target_uids_to_emote.append(int(bot_uid))

                                            for tuid in target_uids_to_emote:
                                                for _ in range(2):
                                                    emote_pkt = await Emote_k(tuid, int(emote_id), key, iv, region)
                                                    if emote_pkt and online_writer:
                                                        online_writer.write(emote_pkt)
                                                        await online_writer.drain()
                                                    await asyncio.sleep(0.05)
                                                print(f"🎭 Title Reply: Emote {emote_id} sent 2 times to {tuid}")

                            except Exception:
                                pass
                except Exception:
                    pass

                clean_msg = inPuTMsG.strip()

                if str(uid) == str(admin_uid):
                    if clean_msg.isdigit() and 7 <= len(clean_msg) <= 10:
                        current_squad_code = clean_msg
                        print(f"💾 [AUTO-SAVE] Short team code '{clean_msg}' saved from chat!")
                        await safe_send_message(XX, f"[B][C][00FF00]✓ Team Code Saved: {clean_msg}", uid, chat_id, key, iv)
                        continue
                    
                    elif clean_msg.startswith("/setcode "):
                        parts = clean_msg.split(" ")
                        if len(parts) >= 2 and parts[1].isdigit():
                            current_squad_code = parts[1]
                            print(f"💾 [AUTO-SAVE] Team code '{parts[1]}' saved via command!")
                            await safe_send_message(XX, f"[B][C][00FF00]✓ Team Code Saved: {parts[1]}", uid, chat_id, key, iv)
                            continue

                if inPuTMsG.strip().startswith('/evo menu'):
                    try:
                        asyncio.create_task(send_box_menu_sequence(XX, uid, chat_id, key, iv))
                    except Exception as e:
                        print(f"/evo menu error: {e}")
                        await safe_send_message(
                            XX, f"[B][C][FF0000]✗ Menu error: {str(e)[:60]}",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/on':
                    if str(uid) != admin_uid:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Only admin can use /on",
                            uid, chat_id, key, iv
                        )
                    else:
                        bot_enabled = True
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Bot is now ON",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/off':
                    if str(uid) != admin_uid:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Only admin can use /off",
                            uid, chat_id, key, iv
                        )
                    else:
                        bot_enabled = False
                        await safe_send_message(
                            XX, "[B][C][FF0000]⛔ Bot is now OFF",
                            uid, chat_id, key, iv
                        )

                # ⚡ 2ND NEW SYSTEM: REFRESH BOT COMMAND (ADMIN ONLY) ⚡
                elif inPuTMsG.strip() in ('refresh bot', '/refresh bot', '/refresh'):
                    if str(uid) != str(admin_uid):
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Only admin can use refresh bot command.",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FFFF00]🔄 বট রিফ্রেশ প্লিজ ওয়েট...",
                            uid, chat_id, key, iv
                        )
                        await asyncio.sleep(1.0)
                        await refresh_bot_state()
                        try:
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except Exception as e:
                            print(f"Restart error: {e}")

                elif inPuTMsG.strip() in ("/help", "/hello", "/bot", "/yasin bhai"):
                    h1_color = get_random_color()
                    h2_color = get_random_color()
                    h3_color = get_random_color()
                    h4_color = get_random_color()
                    h5_color = get_random_color() 
                    h6_color = get_random_color()
                    h7_color = get_random_color() 
                    h8_color = get_random_color()

                    h1 = f"""[B]{h1_color}╭━〔 1 JOIN COMMONS 〕━╮
[C][B][FFFFFF]┣ ➤ /join <code> [00FFFF]» Join Squad
[C][B][FFFFFF]┣ ➤ /exit [00FFFF]» Leave Squad & Reset
[C][B][FFFFFF]┣ ➤ /spam <uid> [00FFFF]» Send Requests
[C][B][FFFFFF]┣ ➤ /stop <uid> [00FFFF]» Stop Requests
[C][B][FFFFFF]┣ ➤ /5 [00FFFF]» 5 Group Player
[C][B][FFFFFF]┣ ➤ /s1 [00FFFF]» Craftland Badge Spam 
[C][B][FFFFFF]┣ ➤ /s2 [00FFFF]» New V-Badge Spam
[C][B][FFFFFF]┣ ➤ /s3 [00FFFF]» Moderator Badge Spam
[C][B][FFFFFF]┣ ➤ /s4 [00FFFF]» Small V-Badge Spam
[C][B][FFFFFF]┣ ➤ /s5 [00FFFF]» Pro Badge Spam
[B]{h1_color}╰━━━━━━━━━━━━━━━╯"""

                    h2 = f"""[B]{h2_color}╭━〔 2 EMOTE COMMANDS 〕━╮
[C][B][FFFFFF]┣ ➤ /e <uid> <emote> [00FFFF]» Send Emote
[C][B][FFFFFF]┣ ➤ /e <name> [00FFFF]» Named Emote
[C][B][FFFFFF]┣ ➤ /fast <uid> <emote> [00FFFF]» Fast Emote Spam
[C][B][FFFFFF]┣ ➤ /fast_stop <uid> <emote> [00FFFF]» Fast Emote stop
[C][B][FFFFFF]┣ ➤ /evo <uid> <1-21> [00FFFF]» Evo Emote
[C][B][FFFFFF]┣ ➤ /evos [00FFFF]» Evo Emote
[C][B][FFFFFF]┣ ➤ /yevos [00FFFF]» Stop Emote
[C][B][FFFFFF]┣ ➤ /evo menu [00FFFF]» All Evo Emote Menu
[C][B][FFFFFF]┣ ➤ /sticker [00FFFF]» Random Sticker
[B]{h2_color}╰━━━━━━━━━━━━━━━╯"""
                    h3 = f"""[B]{h3_color}╭━〔 3 TITLE+BUNDLE COMMONS 〕━╮
[C][B][FFFFFF]┣ ➤           Bundle Commons        
[C][B][FFFFFF]┣ ➤ /bundle <1-12> [00FFFF]» Send Bundle
[C][B][FFFFFF]┣ ➤ /bundle list [00FFFF]» check to bundle list
[C][B][FFFFFF]┣ ➤ /magic  [00FFFF]» Auto Bundle Send

[C][B][FFFFFF]┣ ➤          Title Commons
[C][B][FFFFFF]┣ ➤ /title [00FFFF]» Send to title
[C][B][FFFFFF]┣ ➤ noob [00FFFF]» Send to noob titles
[C][B][FFFFFF]┣ ➤ /alltitles [00FFFF]» Send to alltitles 
[C][B][FFFFFF]┣ ➤ /title on <1-12> [00FFFF]» Send Title spam
[C][B][FFFFFF]┣ ➤ /title off [00FFFF]» Title spam off
[B]{h3_color}╰━━━━━━━━━━━━━━━╯"""

                    h4 = f"""[B]{h4_color}╭━〔 4 FUN COMMANDS 〕━╮
[C][B][FFFFFF]┣ ➤ /love <name> [00FFFF]» Love Messages
[C][B][FFFFFF]┣ ➤ /gali <name> [00FFFF]» Gaali Messages
[C][B][FFFFFF]┣ ➤ /rt <name> [00FFFF]» Roast
[C][B][FFFFFF]┣ ➤ /praisa <name> [00FFFF]» Praise
[C][B][FFFFFF]┣ ➤ /later <name> [00FFFF]» Love Letter
[C][B][FFFFFF]┣ ➤ /sadlater <name> [00FFFF]» Sad Letter
[C][B][FFFFFF]┣ ➤ /joke [00FFFF]» Joke
[C][B][FFFFFF]┣ ➤ /luck <name> [00FFFF]» Fortune
[C][B][FFFFFF]┣ ➤ /quiz [00FFFF]» Quiz Game
[B]{h4_color}╰━━━━━━━━━━━━━━━╯"""

                    h5 = f"""[B]{h5_color}╭━〔 5 ADMIN COMMONS 〕━╮
[C][B][FFFFFF]┣ ➤ /add <uid> [00FFFF]» Send Friend Request
[C][B][FFFFFF]┣ ➤ /remove <uid> [00FFFF]» Remove Friend
[C][B][FFFFFF]┣ ➤ /guildjoin <id> <uid> <pass> [00FFFF]» Join Guild
[C][B][FFFFFF]┣ ➤ /equip [00FFFF]» Bot Id Hi Emote Auto Equip 
[C][B][FFFFFF]┣ ➤ /mimic_on [00FFFF]» Enable Emote Mimic
[C][B][FFFFFF]┣ ➤ /mimic_off [00FFFF]» Disable Emote Mimic
[C][B][FFFFFF]┣ ➤ /refresh bot [00FFFF]» Restart & Refresh Bot
[B]{h5_color}╰━━━━━━━━━━━━━━━╯"""

                    h6 = f"""[B]{h6_color}╭━〔 6 PILIYA COMMONS 〕━╮
[C][B][FFFFFF]┣ ➤ /like <uid> [00FFFF]» Free Likes 
[C][B][FFFFFF]┣ ➤ /info <uid> [00FFFF]» Player Info
[C][B][FFFFFF]┣ ➤ /ban check <uid> [00FFFF]» My Id Ban Check
[C][B][FFFFFF]┣ ➤ /status <uid> [00FFFF]» Real-time Tracker
[C][B][FFFFFF]┣ ➤ /ai <question> [00FFFF]» AI Assistant
[C][B][FFFFFF]┣ ➤ /mth <expr> [00FFFF]» Calculator
[C][B][FFFFFF]┣ ➤ /roll [00FFFF]» Dice Roll
[C][B][FFFFFF]┣ ➤ /zodiac [00FFFF]» Zodiac
[C][B][FFFFFF]┣ ➤ /weather [00FFFF]» City Weather
[B]{h6_color}╰━━━━━━━━━━━━━━━╯"""

                    h7 = f"""[B]{h7_color}╭━〔 7 ATTACK & OTHERS 〕━╮
[C][B][FFFFFF]┣ ➤ /mg <text> [00FFFF]» Wave Text Spam
[C][B][FFFFFF]┣ ➤ /reject <uid> [00FFFF]» Reject Spam Loop
[C][B][FFFFFF]┣ ➤ /reject_stop [00FFFF]» Stop Reject Spam
[C][B][FFFFFF]┣ ➤ /room <uid> <id> [00FFFF]» Room Spam
[C][B][FFFFFF]┣ ➤ /stop_room [00FFFF]» Stop Room Spam
[C][B][FFFFFF]┣ ➤ /msg <text> <times> [00FFFF]» Color Msg Spam
[C][B][FFFFFF]┣ ➤ /stop msg [00FFFF]» Stop Msg Spam
[B]{h7_color}╰━━━━━━━━━━━━━━━╯"""

                    h8 = f"""[B][C]{h8_color}╭━〔 LUCKY TCP PREMIUM 〕━╮
[B][FFFFFF]┣ TCP BOT » @freefire_ob_55
[B][FFFFFF]┣ GLORY   » @freefire_ob_55
[B][FFFFFF]┣ LEVELUP » @freefire_ob_55
[B][FFFFFF]┣ LIKEBOT » @freefire_ob_55
[B][C]{h8_color}╰━━━━━━━━━━━━━━╯
[B][C]{h8_color}╭━━━〔 CONTACT 〕━━━╮
[B][FFFFFF]┣ Telegram: @freefire_ob_55
[B][C]{h8_color}╰━━━━━━━━━━━━━━━╯"""

                    for m in (h1, h2, h3, h4, h5, h6, h7, h8):
                        try:
                            P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                            if P:
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(HELP_DELAY)
                        except Exception:
                            pass

                elif inPuTMsG.strip() == "/admin":
                    msg = f"""[b][c]{get_random_color()} ═══ LUCKY TCP BOT ═══

[b][c][FFFFFF]🎯 উপলব্ধ বট:
[b][c][FFFFFF]✅ Premium Bots
[b][c][FFFFFF]✅ Glory Bots
[b][c][FFFFFF]✅ Friend Bots
[b][c][FFFFFF]✅ Clan Bots
[b][c][FFFFFF]✅ TCP Online Bots

[b][c][FFFFFF]💎 Dev : [00FFFF]YASIN × BHAIㅤ!!
[b][c][FFFFFF]✈️ Telegram: @freefire_ob_55
[b][c][FFFFFF]✈️ Channel: @freefireob51

[b][c]{get_random_color()} কিনতে যোগাযোগ করুন!"""
                    P = await SEndMsG(XX, msg, uid, chat_id, key, iv)
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip().startswith('/s1'):
                    await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s2'):
                    await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s3'):
                    await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s4'):
                    await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s5'):
                    await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, XX)
                    
                elif inPuTMsG.strip().startswith('/5') and not inPuTMsG.strip().startswith('/50'):
                    try:
                        await safe_send_message(
                            XX,
                            f"[B][C]{get_random_color()}\n\n» 5 Pʟᴀʏᴇʀꜱ Gʀᴩ Cʀᴇᴀᴛɪɴɢ...",
                            uid, chat_id, key, iv
                        )
                        
                        # প্রথমে নিশ্চিত করতে বট আগের কোনো স্কোয়াডে থাকলে এক্সিট হয়ে যাবে
                        try:
                            exit_old = await ExiT(None, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', exit_old)
                            await asyncio.sleep(0.1)
                        except Exception:
                            pass

                        # Step 1: Bot opens new squad
                        PAc = await OpEnSq_new(key, iv, region) # অথবা OpEnSq(key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                        await asyncio.sleep(0.3)

                        # Step 2: Upgrade squad to 5 slots
                        captain = int(bot_uid) if bot_uid else int(uid)
                        C = await cHSq_new(5, captain, key, iv, region) # অথবা cHSq(5, captain, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                        print(f"[TEAM5] Upgrade packet sent with captain={captain}")
                        await asyncio.sleep(0.3)

                        # Step 3: Fast Invite sending
                        for attempt in range(2):
                            V = await SEnd_InV_new(5, uid, key, iv, region) # অথবা SEnd_InV(5, uid, key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            print(f"[TEAM5] Fast Invite attempt {attempt+1} → uid={uid}")
                            await asyncio.sleep(0.2)

                        # ⭐ ইনভাইট ধরার জন্য ৪ সেকেন্ড সময় দেওয়া হলো (যাতে আপনি গ্রুপে জয়েন করতে পারেন)
                        await asyncio.sleep(3.3)

                        # Step 4: আপনি গ্রুপে ঢোকার পর বট গ্রুপ ছেড়ে বেরিয়ে যাবে
                        E = await ExiT(None, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)

                        await safe_send_message(
                            XX,
                            "[B][C][00FF00]✅ 5 Pʟᴀʏᴇʀ Gʀᴩ Cʀᴇᴀᴛᴇᴅ & Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!",
                            uid, chat_id, key, iv
                        )
                    except Exception as e:
                        print(f"Team5 error: {e}")
                        await safe_send_message(
                            XX,
                            f"[B][C][FF0000]❌ Team5 error: {str(e)[:80]}",
                            uid, chat_id, key, iv
                        )

                    
                elif inPuTMsG.startswith('/join '):
                    try:
                        code = inPuTMsG.split('/join ')[1].strip()
                        current_squad_code = code
                        
                        EM = await JoinSq_original(code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                        await safe_send_message(
                            XX,
                            f"[B]{get_random_color()}✓ Joined squad: {code}",
                            uid, chat_id, key, iv
                        )    
                    except Exception as e:
                        print(f"Join error: {e}")
                        
                elif inPuTMsG.startswith('/exit') or inPuTMsG.startswith('/leave'):
                    # প্রথমে সফলতার মেসেজটি পাঠিয়ে দিন যাতে গ্রুপে থাকা অবস্থাতেই মেসেজটি শো করে
                    await safe_send_message(
                        XX,
                        f"[B]{get_random_color()}✓ Left squad & all glitches/tasks successfully reset!",
                        uid, chat_id, key, iv
                    )
                    
                    # এরপর প্যাকেট সেন্ড করে গ্রুপ থেকে লিভ নিন এবং স্টেট রিসেট করুন
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', await ExiT(uid, key, iv))
                    # ⚡ 1ST NEW SYSTEM: RESET ALL TASKS AND GLITCHES UPON EXIT ⚡
                    await refresh_bot_state()

                elif inPuTMsG.startswith('/spam '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        tgt = parts[1]
                        if tgt in spm_tasks:
                            spm_tasks[tgt].cancel()
                        spam_targets.add(tgt)
                        save_spam_targets()
                        spm_tasks[tgt] = asyncio.create_task(spm_loop(tgt, key, iv))
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]✓ Spam started for {tgt}",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /spam <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.startswith('/stop '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1] in spm_tasks:
                        spm_tasks[parts[1]].cancel()
                        del spm_tasks[parts[1]]
                        if parts[1] in spam_targets:
                            spam_targets.remove(parts[1])
                            save_spam_targets()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Spam stopped",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ No active spam",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.startswith('/gh '):
                    parts = inPuTMsG.split(' ', 2)
                    if len(parts) >= 3 and bot_uid is not None:
                        teamcode = parts[1].strip()
                        name = parts[2].strip()
                        try:
                            await SEndPacKeT(
                                whisper_writer, online_writer, 'OnLine',
                                await JoinSq_original(teamcode, key, iv)
                            )
                            await asyncio.sleep(1.0)
                            
                            for _ in range(4):
                                await SEndPacKeT(
                                    whisper_writer, online_writer, 'OnLine',
                                    await GhostPakcet(bot_uid, name, teamcode, key, iv)
                                )
                                await asyncio.sleep(0.2)
                                
                            await safe_send_message(
                                XX, f"[B][C][FFFFFF]✓ Ghost joined as {name}",
                                uid, chat_id, key, iv
                            )
                        except Exception as e:
                            await safe_send_message(
                                XX, f"[B][C][FF0000]✗ {e}",
                                uid, chat_id, key, iv
                            )

                # NEW CONTROLLED LAG COMMAND
                elif inPuTMsG.strip().startswith('/lag '):
                    print('Processing controlled lag command')
                    
                    parts = inPuTMsG.strip().split()
                    if len(parts) < 2:
                        error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lag <team_code> [times]\nExample: /lag ABC123 5\n"
                        await safe_send_message(XX, error_msg, uid, chat_id, key, iv)
                    else:
                        team_code = parts[1]
                        current_squad_code = team_code
                        
                        # কতবার চলবে তা সেট করা (ডিফল্ট ৫ বার, চাইলে ইউজার বসাতে পারবে)
                        times = 5
                        if len(parts) >= 3 and parts[2].isdigit():
                            times = int(parts[2])
                            if times > 50:  # নিরাপত্তার জন্য সর্বোচ্চ ৩০ বারের বেশি একবারে এলাও করবে না
                                times = 50
                        
                        # Stop any existing lag task
                        if lag_task and not lag_task.done():
                            lag_running = False
                            lag_task.cancel()
                            await asyncio.sleep(0.1)
                        
                        # Start new controlled lag task
                        lag_running = True
                        lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region, max_times=times))
                        
                        # SUCCESS MESSAGE
                        success_msg = f"[B][C][FFFF00]✅ SUCCESS! Safe Lag started!\nTeam: {team_code}\nCycles: {times} times\nAnti-Ban: Protected 🛡️\n"
                        await safe_send_message(XX, success_msg, uid, chat_id, key, iv)

                # STOP LAG COMMAND (যেমন আছে তেমনই থাকবে)
                elif inPuTMsG.strip() in ('/stop lag', '/stop_lag', 'stop lag'):
                    if lag_task and not lag_task.done():
                        lag_running = False
                        lag_task.cancel()
                        success_msg = f"[B][C][FFFF00]✅ SUCCESS! Lag attack stopped successfully!\n"
                        await safe_send_message(XX, success_msg, uid, chat_id, key, iv)
                    else:
                        error_msg = f"[B][C][FF0000]❌ ERROR! No active lag attack to stop!\n"
                        await safe_send_message(XX, error_msg, uid, chat_id, key, iv)

                elif inPuTMsG.startswith('/msg '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) < 3:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /msg <text> <times>",
                            uid, chat_id, key, iv
                        )
                    else:
                        try:
                            times = int(parts[-1])
                            message = ' '.join(parts[1:-1])
                            if msg_spam_task and not msg_spam_task.done():
                                msg_spam_running = False
                                msg_spam_task.cancel()
                                await asyncio.sleep(0.1)
                            msg_spam_running = True
                            msg_spam_task = asyncio.create_task(
                                msg_spam_loop(message, times, chat_id, key, iv, region)
                            )
                            await safe_send_message(
                                XX,
                                f"[B][C][FFFFFF]✓ Sending {times}x: {message}",
                                uid, chat_id, key, iv
                            )
                        except ValueError:
                            await safe_send_message(
                                XX, "[B][C][FF0000]Usage: /msg <text> <times>",
                                uid, chat_id, key, iv
                            )

                elif inPuTMsG.strip() == '/stop msg':
                    if msg_spam_task and not msg_spam_task.done():
                        msg_spam_running = False
                        msg_spam_task.cancel()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Message spam stopped",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.startswith('/mg '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) < 2:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /mg <text> [repeats]",
                            uid, chat_id, key, iv
                        )
                    else:
                        try:
                            message = parts[1]
                            repeats = int(parts[2]) if len(parts) > 2 else 5
                            if repeats > 10:
                                repeats = 10
                            if mg_spam_task and not mg_spam_task.done():
                                msg_spam_running = False
                                mg_spam_task.cancel()
                                await asyncio.sleep(0.1)
                            msg_spam_running = True
                            mg_spam_task = asyncio.create_task(
                                send_wave_messages(message, repeats, chat_id, key, iv, region)
                            )
                            await safe_send_message(
                                XX,
                                f"[B][C][FFFFFF]✓ Wave started: {message} x{repeats}",
                                uid, chat_id, key, iv
                            )
                        except ValueError:
                            await safe_send_message(
                                XX, "[B][C][FF0000]Usage: /mg <text> [repeats]",
                                uid, chat_id, key, iv
                            )

                elif inPuTMsG.strip().startswith('/ban check '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 3 and parts[2].isdigit():
                        try:
                            reply = await check_ban_auto(parts[2])
                        except Exception as e:
                            reply = f"[B][C][FF0000]✗ Error: {e}"
                        P = await SEndMsG(XX, reply, uid, chat_id, key, iv)
                        if P:
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /ban check <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip().startswith('/ban '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        if ban_task and not ban_task.done():
                            ban_running = False
                            ban_task.cancel()
                            ban_targets.clear()
                            await asyncio.sleep(0.3)
                        ban_targets.add(parts[1])
                        ban_task = asyncio.create_task(ban_loop(key, iv))
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]✓ Ban started on {parts[1]}",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /ban <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/reject' or inPuTMsG.strip().startswith('/reject '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        if reject_spam_task and not reject_spam_task.done():
                            reject_spam_running = False
                            reject_spam_task.cancel()
                            await asyncio.sleep(0.3)
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]🌀 Reject spam started on {parts[1]}",
                            uid, chat_id, key, iv
                        )
                        reject_spam_running = True
                        reject_spam_task = asyncio.create_task(
                            reject_spam_loop(parts[1], key, iv)
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Usage: /reject <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() in ('/reject_stop', '/stop reject'):
                    if reject_spam_task and not reject_spam_task.done():
                        reject_spam_running = False
                        reject_spam_task.cancel()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Reject spam stopped",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ No active reject spam",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.startswith('/evos'):
                    parts = inPuTMsG.strip().split()
                    uids = await resolve_bot_auto_uid(uid, parts[1:])
                    if evo_cycle_task and not evo_cycle_task.done():
                        evo_cycle_running = False
                        evo_cycle_task.cancel()
                        await asyncio.sleep(0.3)
                    evo_cycle_running = True
                    evo_cycle_task = asyncio.create_task(
                        evo_gun_cycle(uids, EVO_IDS, key, iv, region)
                    )
                    await safe_send_message(
                        XX, "[B][C][FFFFFF]✓ Evo Emote started",
                        uid, chat_id, key, iv
                    )

                elif inPuTMsG.strip() == '/yevos':
                    if evo_cycle_task and not evo_cycle_task.done():
                        evo_cycle_running = False
                        evo_cycle_task.cancel()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Evo Emote stopped",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/fast' or inPuTMsG.strip().startswith('/fast '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
                        tgt_uid = parts[1]
                        emote_id = parts[2]
                        if fast_spam_task and not fast_spam_task.done():
                            fast_spam_running = False
                            fast_spam_task.cancel()
                            await asyncio.sleep(0.3)
                        
                        fast_spam_running = True
                        fast_spam_task = asyncio.create_task(
                            fast_emote_spam([tgt_uid], emote_id, key, iv, region)
                        )
                        
                        await safe_send_message(
                            XX, f"[B][C][FFFFFF]✓ Fast spam started safely on {tgt_uid} with emote {emote_id}",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Usage: /fast <uid> <emote>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() in ('/fast_stop', '/stop fast'):
                    if fast_spam_task and not fast_spam_task.done():
                        fast_spam_running = False
                        fast_spam_task.cancel()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Fast spam stopped safely",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ No active fast spam",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/p ' or inPuTMsG.startswith('/p '):
                    parts = inPuTMsG.strip().split()
                    try:
                        if len(parts) == 3:
                            resolved = await resolve_bot_auto_uid(uid, None)
                            tgt = resolved[0]
                            emote_id = parts[1]
                            times = int(parts[2])
                        elif len(parts) >= 4:
                            tgt = parts[1]
                            emote_id = parts[2]
                            times = int(parts[3])
                        else:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]Usage: /p [uid] <emote> <times>",
                                uid, chat_id, key, iv
                            )
                            continue
                        if times > 100:
                            times = 100
                        if custom_spam_task and not custom_spam_task.done():
                            custom_spam_running = False
                            custom_spam_task.cancel()
                            await asyncio.sleep(0.2)
                        custom_spam_running = True
                        custom_spam_task = asyncio.create_task(
                            custom_emote_spam(tgt, emote_id, times, key, iv, region)
                        )
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]✓ Custom spam started: {emote_id} x{times}",
                            uid, chat_id, key, iv
                        )
                    except ValueError:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /p [uid] <emote> <times>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/e' or inPuTMsG.strip().startswith('/e '):
                    parts = inPuTMsG.strip().split()
                    try:
                        if len(parts) < 2:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]✗ Usage: /e <name> or /e <uid> <name>",
                                uid, chat_id, key, iv
                            )
                            continue
                        last = parts[-1].lower()
                        is_num = last.isdigit() and last in NUMBER_EMOTES
                        is_name = last in NAME_EMOTES or last in NAME_TO_EMOTE_ID
                        if not (is_num or is_name):
                            await safe_send_message(
                                XX,
                                f"[B][C][FF0000]✗ Emote '{last}' not found",
                                uid, chat_id, key, iv
                            )
                            continue
                        if len(parts) == 2:
                            resolved = await resolve_bot_auto_uid(uid, None)
                            tgt_uids = [int(x) for x in resolved]
                        else:
                            tgt_uids = [int(p) for p in parts[1:-1] if p.isdigit() and len(p) >= 7]
                            if not tgt_uids:
                                resolved = await resolve_bot_auto_uid(uid, None)
                                tgt_uids = [int(x) for x in resolved]
                        emote_id = NUMBER_EMOTES.get(last) if is_num else (
                            NAME_EMOTES.get(last) or NAME_TO_EMOTE_ID.get(last)
                        )
                        sc = 0
                        for t in tgt_uids:
                            try:
                                H = await Emote_k(t, int(emote_id), key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                sc += 1
                                await asyncio.sleep(0.1)
                            except Exception:
                                pass
                        if sc > 0:
                            await safe_send_message(
                                XX,
                                f"[B][C][FFFFFF]✓ Sent emote to {sc} people",
                                uid, chat_id, key, iv
                            )
                    except Exception as e:
                        print(f"E cmd error: {e}")

                elif inPuTMsG.strip() == '/evo' or (inPuTMsG.strip().startswith('/evo ') and not inPuTMsG.strip().startswith('/evos')):
                    parts = inPuTMsG.strip().split()
                    try:
                        num = None
                        uids_l = []
                        for p in parts[1:]:
                            if p.isdigit():
                                if len(p) <= 2 and num is None:
                                    num = p
                                else:
                                    uids_l.append(p)
                        if not num:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]✗ Usage: /evo [uid] <1-21>",
                                uid, chat_id, key, iv
                            )
                            continue
                        if not uids_l:
                            uids_l = await resolve_bot_auto_uid(uid, None)
                        num_i = int(num)
                        if num_i not in EMOTE_MAP:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]✗ Number must be between 1-21",
                                uid, chat_id, key, iv
                            )
                            continue
                        emote_id = EMOTE_MAP[num_i]
                        for t in uids_l:
                            try:
                                H = await Emote_k(int(t), int(emote_id), key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                await asyncio.sleep(0.1)
                            except Exception:
                                pass
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]✓ Sent evo emote {num_i}",
                            uid, chat_id, key, iv
                        )
                    except Exception as e:
                        print(f"Evo error: {e}")
                       
                elif inPuTMsG.strip().startswith('/title on'):
                    global title_loop_running, title_loop_task
                    parts = inPuTMsG.strip().split()
                    
                    titles_12 = [
                        905090075, 904990072, 904990069, 905190079, 
                        904090014, 904090015, 904090024, 904090025, 
                        904090026, 904090027, 904990070, 904990071
                    ]
                    
                    if len(parts) >= 3 and parts[2].isdigit():
                        t_num = int(parts[2])
                        if 1 <= t_num <= 12:
                            selected_title_id = titles_12[t_num - 1]
                            
                            # যদি আগের কোনো টাস্ক চলতে থাকে তবে তা বন্ধ করা
                            if title_loop_task and not title_loop_task.done():
                                title_loop_running = False
                                title_loop_task.cancel()
                                await asyncio.sleep(0.2)
                                
                            title_loop_running = True
                            target_for_title = uid
                            title_loop_task = asyncio.create_task(
                                title_spam_loop(target_for_title, chat_id, key, iv, region, XX, selected_title_id)
                            )
                            
                            await safe_send_message(
                                XX, 
                                f"[B][C][00FF00]✓ Title #{t_num} continuous spam started! (Interval: 1.5s)\n[C][FFFFFF]Type [FFFF00]/title off [FFFFFF]to stop.", 
                                uid, chat_id, key, iv
                            )
                        else:
                            await safe_send_message(
                                XX, 
                                "[B][C][FF0000]✗ Please choose a title number between 1 and 12!\nExample: /title on 3", 
                                uid, chat_id, key, iv
                            )
                    else:
                        await safe_send_message(
                            XX, 
                            "[B][C][FF0000]✗ Usage: /title on <1-12>\n", 
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() in ('/title off', '/title_off', 'title off'):
                    if title_loop_task and not title_loop_task.done():
                        title_loop_running = False
                        title_loop_task.cancel()
                        await safe_send_message(
                            XX, 
                            "[B][C][00FF00]✓ Title continuous spam stopped successfully!", 
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, 
                            "[B][C][FF0000]✗ No active title spam running!", 
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip().startswith('/title') or inPuTMsG.strip().startswith('/alltitles') or inPuTMsG.strip().startswith('noob'):
                    cmd = inPuTMsG.strip().lower()
                    mode_type = "12" if cmd.startswith('/alltitles') else "9"
                    
                    current_inviter = locals().get('inviter_uid') or uid
                    
                    try:
                        await send_all_titles_sequentiallly(uid, chat_id, key, iv, region, XX, current_inviter, mode=mode_type)
                    except Exception as e:
                        print(f"Title command error: {e}")

                elif inPuTMsG.strip().lower() == '/bundle list':
                    bundle_list_text = (
                        f"[B][C][00FFFF]╭━〔 📦 AVAILABLE BUNDLES 〕━╮\n"
                        f"[C][FFFFFF]┣ 1 ➤ Rampage\n"
                        f"[C][FFFFFF]┣ 2 ➤ Cannibal\n"
                        f"[C][FFFFFF]┣ 3 ➤ Devil\n"
                        f"[C][FFFFFF]┣ 4 ➤ Scorpio\n"
                        f"[C][FFFFFF]┣ 5 ➤ Frostfire\n"
                        f"[C][FFFFFF]┣ 6 ➤ Paradox\n"
                        f"[C][FFFFFF]┣ 7 ➤ Naruto\n"
                        f"[C][FFFFFF]┣ 8 ➤ Aurora\n"
                        f"[C][FFFFFF]┣ 9 ➤ Midnight\n"
                        f"[C][FFFFFF]┣ 10 ➤ Itachi\n"
                        f"[C][FFFFFF]┣ 11 ➤ Dreamspace\n"
                        f"[C][FFFFFF]┣ 12 ➤ Eclipse\n"
                        f"[C][FFFFFF]┣ 13 ➤ Special Elite\n"
                        f"[C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━━━╯\n"
                        f"[C][FFFF00]💡 Usage: /bundle <number> OR /bundle <name>"
                    )
                    await safe_send_message(XX, bundle_list_text, uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/animation'):
                    parts = inPuTMsG.strip().split()
                    anim_ids = {
                        "1": 914000002, "2": 914000003, "3": 914038001,
                        "4": 914039001, "5": 914042001, "6": 914044001,
                        "7": 914047001, "8": 914047002, "9": 914048001,
                        "10": 914050001, "11": 914051001, "12": 914053001
                    }
                    if len(parts) < 2:
                        lst = (
                            "1-rampage\n2-cannibal\n3-devil\n4-scorpio\n5-frostfire\n"
                            "6-paradox\n7-naruto\n8-aurora\n9-midnight\n"
                            "10-itachi\n11-dreamspace\n12-eclipse"
                        )
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]Animations:\n{lst}",
                            uid, chat_id, key, iv
                        )
                    elif parts[1] in anim_ids:
                        try:
                            pkt = await animation_packet(anim_ids[parts[1]], key, iv)
                            if pkt and online_writer:
                                online_writer.write(pkt)
                                await online_writer.drain()
                            await safe_send_message(
                                XX,
                                f"[B][C][FFFFFF]✓ Animation {parts[1]} sent!",
                                uid, chat_id, key, iv
                            )
                        except Exception as e:
                            print(f"Anim error: {e}")
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Animation not found",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip().startswith('/bundle '):
                    parts = inPuTMsG.strip().split()
                    bundle_ids = {
                        "1": 914000002, "rampage": 914000002,
                        "2": 914000003, "cannibal": 914000003,
                        "3": 914038001, "devil": 914038001,
                        "4": 914039001, "scorpio": 914039001,
                        "5": 914042001, "frostfire": 914042001,
                        "6": 914044001, "paradox": 914044001,
                        "7": 914047001, "naruto": 914047001,
                        "8": 914047002, "aurora": 914047002,
                        "9": 914048001, "midnight": 914048001,
                        "10": 914050001, "itachi": 914050001,
                        "11": 914051001, "dreamspace": 914051001,
                        "12": 914053001, "eclipse": 914053001
                    }
                    if len(parts) < 2:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /bundle <1-13> or /bundle <name>",
                            uid, chat_id, key, iv
                        )
                    elif parts[1].lower() in bundle_ids:
                        bid = bundle_ids[parts[1].lower()]
                        try:
                            anim_pkt = await animation_packet(bid, key, iv)
                            if anim_pkt and online_writer:
                                online_writer.write(anim_pkt)
                                await online_writer.drain()
                            await asyncio.sleep(3)
                            b_pkt = await Look_Changer(bid, key, iv, look_type=1, region=region)
                            if b_pkt and online_writer:
                                online_writer.write(b_pkt)
                                await online_writer.drain()
                            await safe_send_message(
                                XX,
                                f"[B][C][FFFFFF]✓ Bundle {parts[1]} sent!",
                                uid, chat_id, key, iv
                            )
                        except Exception as e:
                            print(f"Bundle error: {e}")
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Bundle not found",
                            uid, chat_id, key, iv
                        )
                        
                elif inPuTMsG.strip() == '/magic':
                    global magic_bundle_running, magic_bundle_task
                    if magic_bundle_task and not magic_bundle_task.done():
                        magic_bundle_running = False
                        magic_bundle_task.cancel()
                        await asyncio.sleep(0.2)
                    
                    magic_bundle_task = asyncio.create_task(
                        magic_bundle_loop(chat_id, key, iv, region, XX, uid)
                    )

                elif inPuTMsG.strip().startswith('/sticker'):
                    try:
                        parts = inPuTMsG.strip().split()
                        times = 1
                        if len(parts) >= 2 and parts[1].isdigit():
                            times = int(parts[1])
                            if times > 50:
                                times = 50

                        for _ in range(times):
                            pkt = await send_sticker_packet(uid, chat_id, key, iv)
                            if pkt and whisper_writer:
                                whisper_writer.write(pkt)
                                await whisper_writer.drain()
                                await asyncio.sleep(0.1)
                    except Exception as e:
                        print(f"Sticker error: {e}")

                elif inPuTMsG.strip().startswith('/love '):
                    try:
                        name = inPuTMsG.strip()[6:].strip()
                        msgs = [
                            f"[B][C][FF0066]❤️ {name} তোকে অনেক ভালোবাসি সোনা! তুই আমার জীবনের সব! ❤️",
                            f"[B][C][00FFFF]🔥 {name} তুই এত দারুণ গেমপ্লে দিস যে একা সব এনিমি মেরে ফেলোস! 🔥",
                            f"[B][C][FFFF00]💋 {name} তোর মারাত্মক প্রো গেমপ্লে দেখে তোর প্রেমে পড়ে গেছি বাবু! 😘",
                            f"[B][C][FF3399]💖 {name} আমার বিছানার রানী/রাজা হয়ে যাবি নাকি রাতারাতি? একদম 18+ হট ফিল! 🥵💦",
                            f"[B][C][FF0000]💘 {name} তুই ছাড়া আমার গেমিং লাইফ একদম বেকার রে পাগল! 🌹",
                            f"[B][C][00FF00]💦 {name} তোর সাথে ডুও খেললে বুকটা কেঁপে ওঠে, চলো আজ বেডরুমে সোলো ভার্সেস স্কোয়াড খেলি! 😍🔥",
                            f"[B][C][FF66CC]💕 {name} তুই একে একে সব স্কোয়াড সাফ করে দিস, মারাত্মক লেভেলের সেক্সুয়ালি প্রো প্লেয়ার! 👑🥵"
                        ]
                        for m in msgs:
                            P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print(f"Love error: {e}")

                elif inPuTMsG.strip().startswith('/gali '):
                    try:
                        name = inPuTMsG.strip()[6:].strip()
                        blocked = ["rafin", "rafin txt", "rafin.txt"]
                        if name.lower() in blocked:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]⚠️ Bot owner cannot be targeted!",
                                uid, chat_id, key, iv
                            )
                            continue
                        msgs = [
                            f"[B][C][FF0000]🤬 {name} একটা আস্ত মাদারচোদ, শুয়োরের বাচ্চা! 🖕",
                            f"[B][C][FF6600]💩 {name} তোর গুষ্টির পিণ্ডে আগুন, বাল ছেরা একটা নুবড়া! 💢",
                            f"[B][C][9900FF]🤡 {name} ফালতু গাধা, টয়লেটের পোকা কোথাকার! 🐛",
                            f"[B][C][FF00FF]🔥 {name} তোর মা-কে চুদি, চুমা দে তোর বউকে! 👺",
                            f"[B][C][00FFFF]💀 {name} জন্মের ভুল তুই, জন্মের পর ডাক্তার তোকে ডাস্টবিনে ফেলছিল! 🤬",
                            f"[B][C][FFFF00]⚡ {name} বট কোথাকার, এনিমি দেখলে প্যান্ট ভিজিয়ে ফেলোস! 💩",
                            f"[B][C][FF3399]💢 {name} তোর চৌদ্দগোষ্ঠী গুষ্টি শুদ্ধ চুদি, মাদারজাত একটা! 🖕🔥"
                        ]
                        for m in msgs:
                            P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print(f"Gali error: {e}")

                elif inPuTMsG.strip().startswith('/rt '):
                    try:
                        name = inPuTMsG.strip()[4:].strip()
                        msgs = [
                            f"[B][C][FF0000]😆 {name} ইজ আ বট, একেবারে হাগু মার্কা বট! 🤖",
                            f"[B][C][FF6600]🗿 {name} ট্রেনিং গ্রাউন্ডের সবচেয়ে বড় আবর্জনা ডামি! 🗿",
                            f"[B][C][00FFFF]😂 {name} ফ্রি ফায়ারের ইতিহাসে সবচেয়ে বড় নুব! 🎯"
                        ]
                        for m in msgs:
                            P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print(f"RT error: {e}")

                elif inPuTMsG.strip().startswith('/praisa '):
                    try:
                        name = inPuTMsG.strip()[8:].strip()
                        msgs = [
                            f"[B][C][FFFFFF]🌟 {name} তুই একজন অসাধারণ মানুষ! 🌟",
                            f"[B][C][FFFFFF]🔥 {name} তোর কঠোর পরিশ্রম একদিন অবশ্যই সফল হবে! 🔥",
                            f"[B][C][FFFFFF]💎 {name} তুই একদম ইউনিক, সবার চেয়ে আলাদা! 💎"
                        ]
                        for m in msgs:
                            P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(0.8)
                    except Exception as e:
                        print(f"Praisa error: {e}")

                elif inPuTMsG.strip().startswith('/later '):
                    try:
                        name = inPuTMsG.strip()[7:].strip()
                        msg = (
                            f"[B][C][FF0000]💌 প্রিয় {name} 💌\n\n"
                            f"তোর স্মৃতির পাতা জুড়ে কাটে আমার দিন,\n"
                            f"তোকে ছাড়া এই মন কাঁদে প্রতিদিন।\n\n"
                            f"💕 চিরকাল তোরই 💕"
                        )
                        P = await SEndMsG(XX, msg, uid, chat_id, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    except Exception as e:
                        print(f"Later error: {e}")

                elif inPuTMsG.strip().startswith('/sadlater '):
                    try:
                        name = inPuTMsG.strip()[10:].strip()
                        msg = (
                            f"[B][C][FFFFFF]💔 {name} 💔\n\n"
                            f"একবার শোন না এই ভাঙা হৃদয়ের ডাক,\n"
                            f"প্রতিটি রাতে তোকেই শুধু মনে পড়ে যাক。\n\n"
                            f"💔 বড্ড একা 💔"
                        )
                        P = await SEndMsG(XX, msg, uid, chat_id, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    except Exception as e:
                        print(f"Sad error: {e}")

                elif inPuTMsG.strip() == '/joke':
                    jokes = [
                        "শিক্ষক: তুই হোমওয়ার্ক করিসনি কেন?\nছাত্র: স্যার, কারেন্ট চলে গেছিল তো।\nশিক্ষক: দিনে করিসনি কেন?\nছাত্র: দিনে তো আমার ঘুম পায় স্যার!\n🤣",
                        "স্ত্রী: ওগো একটা কথা বল তো!\nস্বামী: বলো সোনা।\nস্ত্রী: আমি বেশি সুন্দর নাকি তোমার মা?\nস্বামী: দুজনেই দারুণ সুন্দর গো!\n😂"
                    ]
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]😂 মজার জোকস 😂\n\n{random.choice(jokes)}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() == '/dare':
                    dares = [
                        '🔥 ৫ মিনিট চোখ বন্ধ করে বসে থাক!',
                        '😂 পরের ১০ মিনিট শুধু হা হা করে হাসবি!',
                        '🐔 মুরগির মতো ডাক দিয়ে দেখা দেখি!'
                    ]
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🎲 ডেয়ার চ্যালেঞ্জ 🎲\n\n{random.choice(dares)}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() == '/truth':
                    truths = [
                        '💕 তুই কাকে মনে প্রাণে সবচেয়ে বেশি ভালোবাসিস?',
                        '🤫 তোর জীবনের সবচেয়ে বড় গোপন কথাটা কী?',
                        '💔 কার প্রেমে পাগল হয়ে আছিস বল?'
                    ]
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🤔 ট্রুথ গেম 🤔\n\n{random.choice(truths)}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() == '/wyr':
                    a, b = random.choice([
                        ("অদৃশ্য হয়ে যাওয়ার ক্ষমতা", "আকাশে ওড়ার ক্ষমতা"),
                        ("সুপারম্যান হওয়া", "ব্যাটম্যান হওয়া")
                    ])
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🤔 তুমি কোনটা বেছে নেবে?\n\nএ) {a}\n\nবি) {b}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() == '/quiz':
                    q, a = random.choice([
                        ("বাংলাদেশের রাজধানী কোথায়?", "ঢাকা"),
                        ("১ কিলোমিটারে কত মিটার?", "১০০০")
                    ])
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🧠 কুইজ গেম 🧠\n\n❓ প্রশ্ন: {q}\n\n✓ সঠিক উত্তর: {a}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() == '/roll':
                    d1, d2 = random.randint(1, 6), random.randint(1, 6)
                    faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🎲 ছক্কা গেম 🎲\n\n🎯 প্রথম ছক্কা: {faces[d1]} {d1}\n🎯 দ্বিতীয় ছক্কা: {faces[d2]} {d2}\n\n📊 মোট যোগফল: {d1 + d2}/১২",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() in ('/zodiac', '/rashi'):
                    signs = {
                        "মেষ রাশি ♈": ("লাল", "৯", "মঙ্গলবার"),
                        "বৃষ রাশি ♉": ("সবুজ", "৬", "শুক্রবার")
                    }
                    s, d = random.choice(list(signs.items()))
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🌟 রাশিফল 🌟\n\n🔮 রাশি: {s}\n🎨 লাকি কালার: {d[0]}\n🔢 লাকি নম্বর: {d[1]}\n📅 শুভ দিন: {d[2]}\n\n📜 {random.choice(['আজকের দিনটি আপনার খুব চমৎকার কাটবে!', 'আজ প্রেমের ক্ষেত্রে দারুণ কোনো শুভ সংবাদ পেতে পারেন!'])}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip() in ('/weather', '/abohawa'):
                    city = random.choice(["ঢাকা", "চট্টগ্রাম", "সিলেট", "রাজশাহী"])
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🌤️ আবহাওয়া 🌤️\n\n📍 শহর: {city}\n🌡️ তাপমাত্রা: {random.randint(20, 40)}°C\n☁️ আবহাওয়া অবস্থা: {random.choice(['☀️ রোদোজ্জ্বল', '🌤️ আংশিক মেঘলা', '🌧️ বৃষ্টিমুখর'])}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip().startswith('/luck '):
                    name = inPuTMsG.strip()[6:].strip().title()
                    P = await SEndMsG(
                        XX,
                        f"[B][C][FFFFFF]🔮 ভাগ্য পরীক্ষা 🔮\n\n👤 নাম: {name}\n\n{random.choice([f'🌟 {name}, খুব শীঘ্রই তুই বিশাল বড় সফলতা অর্জন করবি!', f'💰 {name}, তোর জীবনে প্রচুর টাকা-পয়সা ও ধন-সম্পদ আসতে চলেছে!'])}",
                        uid, chat_id, key, iv
                    )
                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip().startswith('/like'):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        target_uid = parts[1]
                    else:
                        await safe_send_message(
                            XX,
                            "[B][C][FF0000]❌ Usage: /like <uid>\n"
                            "[C][FFFFFF]Example: /like 123456789",
                            uid, chat_id, key, iv
                        )
                        target_uid = None

                    if target_uid:
                        asyncio.create_task(
                            run_like_system(target_uid, XX, chat_id, key, iv, uid)
                        )

                elif inPuTMsG.strip().startswith('/info '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]🔍 Fetching info for {parts[1]}...",
                            uid, chat_id, key, iv
                        )
                        try:
                            ok, data = await get_player_info(parts[1])
                            if ok:
                                m1, m2, m3 = format_player_info(data)
                                for m in (m1, m2, m3):
                                    P = await SEndMsG(XX, m, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    await asyncio.sleep(0.5)
                            else:
                                await safe_send_message(
                                    XX, f"[B][C][FF0000]❌ {data}",
                                    uid, chat_id, key, iv
                                )
                        except Exception as e:
                            await safe_send_message(
                                XX, f"[B][C][FF0000]❌ Error: {e}",
                                uid, chat_id, key, iv
                            )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]Usage: /info <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip().startswith('/status'):
                    parts = inPuTMsG.strip().split()
                    if len(parts) < 2 or not parts[1].isdigit():
                        await safe_send_message(
                            XX,
                            "[B][C][FF0000]✗ Usage: /status <uid>",
                            uid, chat_id, key, iv
                        )
                    else:
                        target_uid = parts[1]
                        clear_cache_entry(target_uid)

                        await safe_send_message(
                            XX,
                            f"[B][C][FFFF00]🔍 Checking status for {fix_num(target_uid)}...",
                            uid, chat_id, key, iv
                        )
                        try:
                            status_packet = await createpacketinfo(target_uid, key, iv)
                            
                            if not status_packet:
                                await safe_send_message(
                                    XX,
                                    "[B][C][FF0000]✗ Failed to create status packet!\n",
                                    uid, chat_id, key, iv
                                )
                            else:
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
                                response_received = False
                                for attempt in range(12):
                                    cache_data = load_from_cache(target_uid)
                                    if cache_data:
                                        response_received = True
                                        status_msg = (
                                            f"[B][C][FFFF00]📊 PLAYER STATUS\n"
                                            f"────────────────\n"
                                            f"👤 UID: {fix_num(target_uid)}\n"
                                            f"📊 Status: {cache_data['status']}\n"
                                        )
                                        if "IN ROOM" in cache_data['status'] and 'room_id' in cache_data:
                                            status_msg += f"🏠 Room ID: {fix_num(cache_data['room_id'])}\n"
                                        elif "INSQUAD" in cache_data['status'] and 'leader_id' in cache_data:
                                            status_msg += f"👑 Leader: {fix_num(cache_data['leader_id'])}\n"
                                        elif "OFFLINE" in cache_data['status']:
                                            status_msg += "🔴 Player is offline\n"
                                        elif "INGAME" in cache_data['status']:
                                            status_msg += "🎮 Player is in match\n"
                                        elif "SOLO" in cache_data['status']:
                                            status_msg += "👤 Player is solo\n"
                                        status_msg += "────────────────\n✓ Real-time data\n"
                                        await safe_send_message(XX, status_msg, uid, chat_id, key, iv)
                                        break
                                    await asyncio.sleep(0.5)
                                    
                                if not response_received:
                                    error_msg = (
                                        f"[B][C][FF0000]✗ STATUS CHECK FAILED\n"
                                        f"👤 UID: {fix_num(target_uid)}\n"
                                        f"📛 No response from server\n"
                                    )
                                    await safe_send_message(XX, error_msg, uid, chat_id, key, iv)
                        except Exception as e:
                            log_error_to_file(str(e), context="Status Command Handler")
                            await safe_send_message(
                                XX, f"[B][C][FF0000]✗ Error: {str(e)[:50]}\n",
                                uid, chat_id, key, iv
                            )

                elif inPuTMsG.strip() == '/ai' or inPuTMsG.strip() == '/ai ':
                    await safe_send_message(
                        XX, "[B][C][FF0000]Usage: /ai <hi>",
                        uid, chat_id, key, iv
                    )
                elif inPuTMsG.strip().startswith('/ai '):
                    question = inPuTMsG.strip()[4:].strip()
                    if question:
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]🤖 AI is thinking...",
                            uid, chat_id, key, iv
                        )
                        try:
                            api_url = f"https://ai-api-free.vercel.app/ask?key=YASIN-BHAI&message={question}"
                            
                            async with aiohttp.ClientSession() as session:
                                async with session.get(
                                    api_url,
                                    timeout=aiohttp.ClientTimeout(total=45)
                                ) as r:
                                    response_text = await r.text()

                                    if r.status == 200:
                                        answer = response_text.strip().replace("[", "(").replace("]", ")")
                                        msg = f"[B][C][FFFFFF]🤖 AI Answer:\n\n[FFFFFF]{answer}"
                                    else:
                                        msg = f"[B][C][FF0000]✗ API Error {r.status}: {response_text[:150]}"
                        except Exception as e:
                            msg = f"[B][C][FF0000]✗ System Error: {str(e)[:100]}"

                        P = await SEndMsG(XX, msg, uid, chat_id, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip().startswith('/mth'):
                    parts = inPuTMsG.strip().split(maxsplit=1)
                    if len(parts) < 2:
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]Usage: /mth <expr>",
                            uid, chat_id, key, iv
                        )
                    else:
                        expr = parts[1].strip().replace("×", "*").replace("÷", "/").replace("x", "*")
                        try:
                            import re as _re
                            if not _re.match(r'^[\d\s\+\-\*\/\.\(\)\%]+$', expr):
                                raise ValueError("Invalid")
                            result = eval(expr)
                            if isinstance(result, float) and result == int(result):
                                result = int(result)
                            P = await SEndMsG(
                                XX,
                                f"[B][C][FFFFFF]🧮 Calculator\n\nExpression: {expr}\nResult: {result}",
                                uid, chat_id, key, iv
                            )
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        except Exception:
                            await safe_send_message(
                                XX, "[B][C][FF0000]✗ Invalid expression",
                                uid, chat_id, key, iv
                            )

                elif inPuTMsG.strip().startswith("/add"):
                    if str(uid) != str(admin_uid):
                        await safe_send_message(
                            XX,
                            f"[B][C][FF0000]✗ Only Admin can use this command!\n"
                            f"[FFFFFF]Your UID: [FFFF00]{uid}\n"
                            f"[FFFFFF]Required Admin UID: [FFFF00]{admin_uid}",
                            uid, chat_id, key, iv
                        )
                    else:
                        parts = inPuTMsG.strip().split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            try:
                                await safe_send_message(XX, "[B][C][FFFF00]⏳ Sending friend request...", uid, chat_id, key, iv)
                                ok, msg = await send_friend_request(parts[1], ToKen, region)
                                reply = f"[B][C][FF66CC]{msg}"
                            except Exception as e:
                                reply = f"[B][C][FF0000]Error: {e}"
                        else:
                            reply = "[B][C][FF0000]Usage: /add <uid>"
                        P = await SEndMsG(XX, reply, uid, chat_id, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                elif inPuTMsG.strip().startswith("/remove"):
                    if str(uid) != str(admin_uid):
                        await safe_send_message(
                            XX,
                            f"[B][C][FF0000]✗ Only Admin can use this command!\n"
                            f"[FFFFFF]Your UID: [FFFF00]{uid}\n"
                            f"[FFFFFF]Required Admin UID: [FFFF00]{admin_uid}",
                            uid, chat_id, key, iv
                        )
                    else:
                        parts = inPuTMsG.strip().split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            try:
                                await safe_send_message(XX, "[B][C][FFFF00]⏳ Removing friend...", uid, chat_id, key, iv)
                                ok, msg = await remove_friend(parts[1], ToKen, region)
                                reply = f"[B][C][FFD700]{msg}"
                            except Exception as e:
                                reply = f"[B][C][FF0000]Error: {e}"
                        else:
                            reply = "[B][C][FF0000]Usage: /remove <uid>"
                        P = await SEndMsG(XX, reply, uid, chat_id, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                elif inPuTMsG.strip().startswith("/guildjoin"):
                    if str(uid) != str(admin_uid):
                        await safe_send_message(
                            XX,
                            f"[B][C][FF0000]✗ Only Admin can use this command!\n"
                            f"[FFFFFF]Your UID: [FFFF00]{uid}\n"
                            f"[FFFFFF]Required Admin UID: [FFFF00]{admin_uid}",
                            uid, chat_id, key, iv
                        )
                    else:
                        # এখানে inPuTMsG এর বদলে msg_raw ব্যবহার করা হয়েছে যাতে বড়/ছোট হাতের অক্ষর ঠিক থাকে
                        parts = msg_raw.strip().split() 
                        
                        if len(parts) >= 4 and parts[1].isdigit() and parts[2].isdigit():
                            guild_id = parts[1]
                            target_uid = parts[2]
                            password = parts[3]  # এখন পাসওয়ার্ড ঠিক তার অরিজিনাল ফর্মে যাবে
                            
                            await safe_send_message(XX, "[B][C][FFFF00]⏳ Connecting to API...", uid, chat_id, key, iv)
                            
                            ok, msg = await join_guild(guild_id, target_uid, password)
                            if ok:
                                reply = f"[B][C][00FF00]✓ {msg}"
                            else:
                                reply = f"[B][C][FF0000]✗ {msg}"
                        else:
                            reply = "[B][C][FF0000]Usage: /guildjoin <guild_id> <uid> <password>"
                            
                        P = await SEndMsG(XX, reply, uid, chat_id, key, iv)
                        if P:
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)


                elif inPuTMsG.strip() == '/equip':
                    await equip_hi_emote(uid, chat_id, XX, key, iv, region)
                elif inPuTMsG.strip() == '/mimic_on':
                    emote_hijack = True
                    await safe_send_message(
                        XX, "[B][C][FF0000]The Mimic Is Now On",
                        uid, chat_id, key, iv
                    )
                elif inPuTMsG.strip() == '/mimic_off':
                    emote_hijack = False
                    await safe_send_message(
                        XX, "[B][C][FF0000]The Mimic Is Now OFF",
                        uid, chat_id, key, iv
                    )

                elif inPuTMsG.strip() == '/ice' or inPuTMsG.strip().startswith('/ice '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2:
                        if parts[1].lower() in ('me', 'self', 'auto'):
                            resolved = await resolve_bot_auto_uid(uid, None)
                            tgt = resolved[0]
                        elif parts[1].isdigit():
                            tgt = parts[1]
                        else:
                            await safe_send_message(
                                XX, "[B][C][FF0000]✗ Usage: /ice <uid>",
                                uid, chat_id, key, iv
                            )
                            continue
                        if freeze_task and not freeze_task.done():
                            freeze_running = False
                            freeze_task.cancel()
                            await asyncio.sleep(0.3)
                        freeze_running = True
                        freeze_task = asyncio.create_task(
                            freeze_emote_spam(tgt, key, iv, region, XX, chat_id, uid)
                        )
                        await safe_send_message(
                            XX,
                            f"[B][C][FFFFFF]❄️ Freeze started on {tgt}",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ Usage: /ice <uid>",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() in ('/ice_stop', '/stop ice'):
                    if freeze_task and not freeze_task.done():
                        freeze_running = False
                        freeze_task.cancel()
                        await safe_send_message(
                            XX, "[B][C][FFFFFF]✓ Freeze stopped",
                            uid, chat_id, key, iv
                        )
                    else:
                        await safe_send_message(
                            XX, "[B][C][FF0000]✗ No active freeze spam",
                            uid, chat_id, key, iv
                        )

                elif inPuTMsG.strip() == '/room' or inPuTMsG.strip().startswith('/room '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) < 3:
                        await safe_send_message(
                            XX,
                            "[B][C][FF0000]Usage: /room <uid> <rid>",
                            uid, chat_id, key, iv
                        )
                    else:
                        tgt, rid = parts[1], parts[2]
                        if not (tgt.isdigit() and rid.isdigit()):
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]Usage: /room <uid> <rid>",
                                uid, chat_id, key, iv
                            )
                        else:
                            if rid in room_spam_tasks:
                                room_spam_tasks[rid].cancel()
                            room_spam_targets[rid] = {"tgt": tgt, "rid": rid}
                            save_room_spam_targets()
                            room_spam_tasks[rid] = asyncio.create_task(
                                room_spam_worker(tgt, rid, key, iv, XX, chat_id, uid)
                            )

                elif inPuTMsG.strip() in ('/room_stop', '/stop_room', '/stop room', 'room stop') or inPuTMsG.strip().startswith(('/stop room ', '/stop_room ')):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 3 and parts[2].isdigit():
                        rid = parts[2]
                        if rid in room_spam_tasks:
                            room_spam_tasks[rid].cancel()
                            del room_spam_tasks[rid]
                            if rid in room_spam_targets:
                                del room_spam_targets[rid]
                                save_room_spam_targets()
                            await safe_send_message(
                                XX,
                                f"[B][C][00FF00]✓ Room {rid} spam stopped successfully!",
                                uid, chat_id, key, iv
                            )
                        else:
                            await safe_send_message(
                                XX,
                                f"[B][C][FF0000]✗ No active room spam found for ID {rid}!",
                                uid, chat_id, key, iv
                            )
                    else:
                        if room_spam_tasks:
                            for rid, task in list(room_spam_tasks.items()):
                                task.cancel()
                            room_spam_tasks.clear()
                            room_spam_targets.clear()
                            save_room_spam_targets()
                            await safe_send_message(
                                XX,
                                "[B][C][00FF00]✓ All Room spams stopped successfully!",
                                uid, chat_id, key, iv
                            )
                        else:
                            await safe_send_message(
                                XX,
                                "[B][C][FF0000]✗ No active room spam found!",
                                uid, chat_id, key, iv
                            )

                elif inPuTMsG.strip().isdigit() or (
                    inPuTMsG.strip().count('*') == 1 and
                    all(p.isdigit() for p in inPuTMsG.strip().split('*'))
                ):
                    number_part = inPuTMsG.strip()
                    emote_id = None
                    times = 1
                    if '*' in number_part:
                        parts = number_part.split('*')
                        number = parts[0]
                        times = min(int(parts[1]), 100)
                    else:
                        number = number_part
                    if number in NUMBER_EMOTES:
                        emote_id = NUMBER_EMOTES[number]
                    elif number.isdigit() and 900_000_000 <= int(number) <= 999_999_999:
                        emote_id = int(number)
                    if emote_id:
                        try:
                            await safe_send_message(
                                XX,
                                "[B][C][FAFAFA] ✓ Sent emote to people",
                                uid, chat_id, key, iv
                            )
                            resolved = await resolve_bot_auto_uid(uid, None)
                            for _ in range(times):
                                for t in resolved:
                                    H = await Emote_k(int(t), int(emote_id), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                    await asyncio.sleep(0.05)
                            print(f"✓ Number emote: {number} → {emote_id} x{times}")
                        except Exception as e:
                            print(f"Number emote error: {e}")

                elif inPuTMsG.strip().lower() in NAME_TO_EMOTE_ID:
                    try:
                        emote_id = NAME_TO_EMOTE_ID[inPuTMsG.strip().lower()]
                        resolved = await resolve_bot_auto_uid(uid, None)
                        for t in resolved:
                            H = await Emote_k(int(t), int(emote_id), key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                        print(f"✓ Name emote: {inPuTMsG.strip()} → {emote_id}")
                    except Exception as e:
                        print(f"Name emote error: {e}")

                else:
                    if inPuTMsG.strip().startswith('/') and len(inPuTMsG.strip()) > 2:
                        pass

            writer.close()
            await writer.wait_closed()
            whisper_writer = None
        except Exception as e:
            log_error_to_file(str(e), context="TcPChaT Connection")
            print(f"Chat connection error: {ip}:{port} - {e} -> Auto-reconnecting & refreshing...")
            whisper_writer = None
            await refresh_bot_state()
        await asyncio.sleep(reconnect_delay)


# ═══════════════════════════════════════════════════════════════
# LEGACY SQUAD / CHAT PACKETS
# ═══════════════════════════════════════════════════════════════

async def OpEnSq(K, V, region):
    fields = {
        1: 1,
        2: {
            2: "\u0001", 3: 1, 4: 1, 5: "en",
            9: 1, 11: 1, 13: 1,
            14: {2: 5756, 6: 11, 8: "1.111.5", 9: 2, 10: 4}
        }
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def cHSq(Nu, Uid, K, V, region):
    fields = {
        1: 17,
        2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def SEnd_InV(Nu, Uid, K, V, region):
    fields = {1: 2, 2: {1: int(Uid), 2: region, 4: int(Nu)}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def GenJoinSquadsPacket(code, K, V):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.111.1"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def xSEndMsg(Msg, Tp, Tp2, id, K, V):
    feilds = {
        1: id, 2: Tp2, 3: Tp, 4: Msg, 5: 1735129800, 7: 2,
        9: {
            1: "[FFFFFF]YASIN × BHAI", 2: int(await xBunnEr()), 3: 901048020, 4: 330,
            5: 1001000001, 8: "YASIN × BHAI - C4", 10: 1, 11: 1, 13: {1: 2},
            14: {
                1: 12484827014, 2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            12: 0
        },
        10: "en", 13: {3: 1}
    }
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)


async def xSEndMsgsQ(Msg, id, K, V, region="BD"):
    avatar = await xBunnEr()

    fields = {
        1: id,
        2: id,
        4: Msg,
        5: 1756580149,
        8: 904990072,
        9: {
            1: "[FFFFFF]YASIN × BHAI",
            2: avatar,
            3: 2,
            4: 329,
            5: 1001000001,
            6: 66,
            7: 66,
            8: "YASIN × BHAI - C4",
            9: 66,
            10: 66,
            11: 66,
            12: 66,
            13: {1: 68, 2: 67},
            14: {
                1: 1158053040,
                2: 8,
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        },
        10: "en",
        13: {66: 66, 66: 66},
        14: {
            11: {
                1: 3, 2: 7, 3: 170, 4: 999, 5: 1,
                6: region, 7: 2, 8: 2, 9: 2
            }
        }
    }

    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)


# ═══════════════════════════════════════════════════════════════
# END OF bot_core.py — YASIN × BHAI
# © 2025 YASIN × BHAI — All rights reserved
# ═══════════════════════════════════════════════════════════════
