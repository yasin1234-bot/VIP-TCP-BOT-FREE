# ═══════════════════════════════════════════════════════════════
# app.py — Flask + SocketIO web server
# Deployable on Render.com / Railway.app
# ═══════════════════════════════════════════════════════════════

import os
import asyncio
from functools import wraps
from flask import (
    Flask, render_template, request, jsonify,
    session, redirect, url_for
)
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import database as db
import bot_manager

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "yasin-bhai-super-secret-2026-change-me")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False   # True on HTTPS

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"ok": False, "error": "Not logged in"}), 401
        return f(*args, **kwargs)
    return wrap


# ═══════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")    
    

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if len(username) < 3:
        return jsonify({"ok": False, "error": "Username must be ≥ 3 characters"})
    if len(password) < 4:
        return jsonify({"ok": False, "error": "Password must be ≥ 4 characters"})

    ok, result = db.create_user(username, password)
    if ok:
        session["user_id"] = result
        session["username"] = username
        return jsonify({"ok": True, "username": username})
    return jsonify({"ok": False, "error": result})


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = db.authenticate(username, password)
    if not user:
        return jsonify({"ok": False, "error": "Invalid username or password"})

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"ok": True, "username": user["username"]})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify({"ok": False, "logged_in": False})
    return jsonify({
        "ok": True,
        "logged_in": True,
        "username": session.get("username"),
        "user_id": session["user_id"]
    })


@app.route("/api/config", methods=["GET"])
@login_required
def api_get_config():
    cfg = db.get_bot_config(session["user_id"])
    running = bot_manager.is_running(session["user_id"])
    return jsonify({
        "ok": True,
        "config": cfg,
        "running": running
    })


@app.route("/api/config", methods=["POST"])
@login_required
def api_save_config():
    data = request.get_json(force=True)
    uid = str(data.get("uid", "")).strip()
    password = str(data.get("password", "")).strip()
    guild_id = str(data.get("guild_id", "")).strip()
    admin_uid = str(data.get("admin_uid", "")).strip()
    region = str(data.get("region", "BD")).strip().upper()

    if not uid or not password:
        return jsonify({"ok": False, "error": "UID and Password are required"})

    db.update_bot_config(session["user_id"], uid, password, guild_id, admin_uid, region)
    return jsonify({"ok": True, "message": "Saved successfully"})


@app.route("/api/bot/start", methods=["POST"])
@login_required
def api_start_bot():
    cfg = db.get_bot_config(session["user_id"])
    if not cfg or not cfg.get("uid") or not cfg.get("password"):
        return jsonify({"ok": False, "error": "Save UID/Password first"})

    ok, msg = bot_manager.start_bot(
        session["user_id"],
        cfg["uid"], cfg["password"],
        cfg.get("guild_id", ""),
        cfg.get("admin_uid", ""),
        cfg.get("region", "BD")
    )
    if ok:
        db.set_bot_running(session["user_id"], True)
    return jsonify({"ok": ok, "message": msg})


@app.route("/api/bot/stop", methods=["POST"])
@login_required
def api_stop_bot():
    ok, msg = bot_manager.stop_bot(session["user_id"])
    db.set_bot_running(session["user_id"], False)
    return jsonify({"ok": ok, "message": msg})


@app.route("/api/bot/logs")
@login_required
def api_logs():
    since = float(request.args.get("since", 0))
    logs = bot_manager.get_logs(session["user_id"], since_ts=since)
    return jsonify({"ok": True, "logs": logs})


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)