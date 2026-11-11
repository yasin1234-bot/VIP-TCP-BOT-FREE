# ═══════════════════════════════════════════════════════════════
# bot_manager.py — Start/stop bot subprocess + stream logs
# ═══════════════════════════════════════════════════════════════

import subprocess
import sys
import os
import threading
import queue
import time

# in-memory running processes {user_id: {...}}
PROCS = {}
LOG_BUFFERS = {}   # {user_id: deque(maxlen=200)}


def _pump_output(user_id, proc, buffer):
    """Read stdout lines → buffer + console."""
    try:
        for raw in iter(proc.stdout.readline, b""):
            line = raw.decode("utf-8", errors="replace").rstrip()
            if line:
                buffer.append((time.time(), line))
                print(f"[user-{user_id}] {line}", flush=True)
    except Exception:
        pass


def start_bot(user_id, uid, password, guild_id, admin_uid, region):
    """Start bot subprocess for a user."""
    if user_id in PROCS and PROCS[user_id]["proc"].poll() is None:
        return False, "Bot already running."

    from collections import deque
    buf = LOG_BUFFERS.setdefault(user_id, deque(maxlen=200))

    cmd = [
        sys.executable, "main.py",
        str(uid), str(password), str(guild_id),
        str(admin_uid), str(region)
    ]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        bufsize=1,
    )
    PROCS[user_id] = {"proc": proc, "started": time.time()}

    t = threading.Thread(
        target=_pump_output,
        args=(user_id, proc, buf),
        daemon=True,
    )
    t.start()

    return True, "Bot started."


def stop_bot(user_id):
    """Terminate subprocess."""
    info = PROCS.get(user_id)
    if not info:
        return False, "No running bot."
    proc = info["proc"]
    if proc.poll() is not None:
        PROCS.pop(user_id, None)
        return False, "Process already dead."
    try:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        PROCS.pop(user_id, None)
        return True, "Bot stopped."
    except Exception as e:
        return False, str(e)


def is_running(user_id):
    info = PROCS.get(user_id)
    return info is not None and info["proc"].poll() is None


def get_logs(user_id, since_ts=0):
    buf = LOG_BUFFERS.get(user_id, [])
    return [{"ts": t, "line": l} for (t, l) in buf if t > since_ts]