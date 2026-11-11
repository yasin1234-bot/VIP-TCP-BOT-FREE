# ═══════════════════════════════════════════════════════════════
# main.py — YASIN × BHAI | WEB-COMPATIBLE REFACTORED
# © 2026 YASIN × BHAI
# ═══════════════════════════════════════════════════════════════

import asyncio
import time
import sys
import os
import httpx

import login_engine
import bot_core

from bot_core import (
    TcPOnLine, TcPChaT,
    build_ob55_online_auth, create_auth_token_chat,
)
from cfonts import render

GUILD_JOIN_API = "https://guild-join-api.vercel.app/join"


def log(level, message):
    icons = {
        "INFO":  ("\033[1;36m", "ℹ"),
        "OK":    ("\033[1;32m", "✔"),
        "WAIT":  ("\033[1;33m", "⏳"),
        "WARN":  ("\033[1;33m", "⚠"),
        "ERROR": ("\033[1;31m", "✘"),
        "BOT":   ("\033[1;35m", "★"),
        "NET":   ("\033[1;36m", "⇄"),
    }
    color, icon = icons.get(level, ("\033[1;37m", "•"))
    reset = "\033[0m"
    ts = time.strftime("%H:%M:%S")
    sys.stdout.write(f"\033[1;90m[{ts}]\033[0m {color}{icon} {level:<5}\033[0m │ {message}\n")
    sys.stdout.flush()


async def join_guild_api(uid, password, guild_id):
    """Guild join API call."""
    params = {"guild_id": str(guild_id), "uid": str(uid), "password": str(password)}
    try:
        async with httpx.AsyncClient(verify=False, timeout=20.0) as c:
            r = await c.get(GUILD_JOIN_API, params=params)
            if r.status_code == 200:
                try:
                    data = r.json()
                    if data.get("success") or data.get("status") in ("ok", "success"):
                        log("OK", f"Guild joined → {data.get('guild_name','?')} ({guild_id})")
                        return True
                except Exception:
                    pass
                log("OK", f"Guild API response: {r.text[:120]}")
                return True
            log("ERROR", f"Guild join failed: HTTP {r.status_code}")
            return False
    except Exception as e:
        log("ERROR", f"Guild join error: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# MAIN BOT RUNNER — callable from web
# ═══════════════════════════════════════════════════════════════
async def run_bot(uid, password, guild_id, admin_uid, region_pref="BD"):
    bot_core.admin_uid = str(admin_uid)              # ✅
    bot_core.BLOCK_EMOTE_UID = str(admin_uid)        # ✅ নতুন যোগ
    bot_core.bot_uid = None
    bot_core.ToKen = None
    bot_core.region = None
    log("BOT", f"Starting bot | admin={admin_uid}")

    # 1. Join guild first (auto)
    if guild_id:
        await join_guild_api(uid, password, guild_id)

    # 2. Login
    async with httpx.AsyncClient(verify=False, timeout=15.0) as client_http:
        vc = await login_engine.version_config(client_http, region_pref)
        if not vc:
            log("ERROR", "Version config failed.")
            return
        release_version, client_version, server_url = vc
        log("OK", f"Version: {client_version} | Release: {release_version}")

        tg = await login_engine.get_access_token(client_http, uid, password)
        if not tg:
            log("ERROR", "Invalid UID/password.")
            return
        open_id, access_token, platform = tg
        log("OK", "Access token acquired.")

        payload = await login_engine.build_majorlogin_payload(
            open_id, access_token, platform, client_version
        )
        if not payload:
            log("ERROR", "Payload creation failed.")
            return

        major_res = await login_engine.send_majorlogin(
            client_http, payload, release_version, server_url
        )
        if not major_res or not major_res.account_uid:
            log("ERROR", "MajorLogin rejected.")
            return
        log("OK", f"Account UID: {major_res.account_uid}")

        gl = await login_engine.send_getlogin(
            client_http, payload, major_res.url, major_res.token, release_version
        )
        if not gl:
            log("ERROR", "GetLoginData failed.")
            return
        res_proto, dict_res = gl

        bot_core.bot_uid = str(major_res.account_uid)
        bot_core.ToKen = major_res.token
        bot_core.region = major_res.region or region_pref

        key = major_res.key or login_engine.AES_KEY
        iv = major_res.iv or login_engine.AES_IV
        timestamp = major_res.timestamp or int(time.time())

        online_addr = res_proto.Online_IP_Port or login_engine.get_proto_field(dict_res, 14, "0.0.0.0:0")
        online_ip, online_port = online_addr.split(":") if ':' in online_addr else ("0.0.0.0", "0")

        chat_addr = res_proto.AccountIP_Port or login_engine.get_proto_field(dict_res, 32, online_addr)
        chat_ip, chat_port = chat_addr.split(":") if ':' in chat_addr else (online_ip, online_port)

        clan_id = res_proto.Clan_ID or 0
        clan_data = res_proto.Clan_Compiled_Data or ""

        ChatAutH = create_auth_token_chat(int(major_res.account_uid), major_res.token, int(timestamp), key, iv)
        OnlineAutH, _ = build_ob55_online_auth(int(major_res.account_uid), major_res.token, int(timestamp), key, iv)

        ready_event = asyncio.Event()
        t1 = asyncio.create_task(
            TcPChaT(chat_ip, chat_port, ChatAutH, key, iv, ready_event,
                    major_res.region or region_pref, clan_id=clan_id, clan_data=clan_data)
        )
        await ready_event.wait()

        t2 = asyncio.create_task(
            TcPOnLine(online_ip, online_port, key, iv, OnlineAutH)
        )

        log("OK", "✅ BOT ONLINE — running...")
        await asyncio.gather(t1, t2)


async def main_forever(uid, password, guild_id, admin_uid, region_pref="BD"):
    """Infinite retry loop."""
    attempt = 0
    while True:
        attempt += 1
        try:
            log("BOT", f"Session #{attempt} starting...")
            await asyncio.wait_for(
                run_bot(uid, password, guild_id, admin_uid, region_pref),
                timeout=7 * 60 * 60
            )
        except asyncio.TimeoutError:
            log("WARN", "Session timeout, reconnecting...")
            await asyncio.sleep(3)
        except Exception as e:
            log("ERROR", f"Runtime: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    # CLI mode (backward-compatible)
    # Usage: python main.py <uid> <pass> <guild> <admin> <region>
    if len(sys.argv) >= 6:
        u, p, g, a, r = sys.argv[1:6]
    else:
        # Fallback: read from uid_pass.txt (single line)
        try:
            with open("uid_pass.txt") as f:
                line = f.readline().strip()
            u, p, g, a, r = line.split("|")
        except Exception:
            print("Usage: python main.py <uid> <pass> <guild> <admin> <region>")
            sys.exit(1)

    asyncio.run(main_forever(u, p, g, a, r))