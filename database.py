# ═══════════════════════════════════════════════════════════════
# database.py — SQLite helper (Users + Bot configs)
# ═══════════════════════════════════════════════════════════════

import sqlite3
import bcrypt
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "yasin_bot.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            uid TEXT DEFAULT '',
            password TEXT DEFAULT '',
            guild_id TEXT DEFAULT '',
            admin_uid TEXT DEFAULT '',
            region TEXT DEFAULT 'BD',
            is_running INTEGER DEFAULT 0,
            started_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def check_pw(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), hashed.encode())
    except Exception:
        return False


def create_user(username, password):
    conn = get_db()
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_pw(password))
        )
        uid = c.lastrowid
        c.execute("INSERT INTO bots (user_id) VALUES (?)", (uid,))
        conn.commit()
        return True, uid
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()


def authenticate(username, password):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    if row and check_pw(password, row["password_hash"]):
        return dict(row)
    return None


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute("SELECT id, username, created_at FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_bot_config(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM bots WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_bot_config(user_id, uid, password, guild_id, admin_uid, region):
    conn = get_db()
    conn.execute("""
        UPDATE bots SET uid=?, password=?, guild_id=?, admin_uid=?, region=?
        WHERE user_id=?
    """, (uid, password, guild_id, admin_uid, region, user_id))
    conn.commit()
    conn.close()


def set_bot_running(user_id, running: bool):
    conn = get_db()
    conn.execute(
        "UPDATE bots SET is_running=?, started_at=? WHERE user_id=?",
        (1 if running else 0,
         datetime.utcnow().isoformat() if running else None,
         user_id)
    )
    conn.commit()
    conn.close()


init_db()