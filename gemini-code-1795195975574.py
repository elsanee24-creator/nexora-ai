import streamlit as st
import base64
import io
import time
import json
import re
import os
import hmac
import sqlite3
import hashlib
import secrets
from pathlib import Path

from groq import Groq
from PIL import Image
from pypdf import PdfReader


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KASHAN'S AI",
    page_icon="✦",
    layout="wide"
)

CHAT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-90b-vision-preview"

# ============================================================
# DATABASE SETUP (USERS, CHATS, NOTES, TASKS)
# ============================================================
DB_PATH = Path("kashan_ai.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            salt TEXT,
            display_name TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            username TEXT,
            title TEXT,
            updated_at REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            image_data TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            content TEXT,
            updated_at REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task TEXT,
            completed INTEGER,
            due_date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
    return pwd_hash, salt

def create_user(username, password, display_name="Kashan"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pwd_hash, salt = hash_password(password)
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, pwd_hash, salt, display_name))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, salt, display_name FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    pwd_hash, salt, display_name = row
    test_hash, _ = hash_password(password, salt)
    if hmac.compare_digest(pwd_hash, test_hash):
        return display_name
    return None

# Ensure default admin user exists
if not verify_user("admin", "admin123"):
    create_user("admin", "admin123", "Kashan King")

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "display_name" not in st.session_state:
    st.session_state.display_name = "Kashan"
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.environ.get("GROQ_API_KEY", "")
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are my-AI, a helpful, intelligent, and friendly AI assistant created by Kashan King. 👑"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Chat"

# ============================================================
# MOBILE APP SIMULATOR HTML (WITH my-AI)
# ============================================================
MOBILE_APP_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box}

:root{
 --mint:#65f5c1;--aqua:#35d8e8;--blue:#668cff;
 --violet:#a77bff;--gold:#ffd477;
 --ink:#102b35;--paper:#f2fff9;--muted:#b9d9d5;
}

html,body{
 margin:0;padding:0;width:100%;min-height:100%;
 font-family:Arial,sans-serif;
 background:linear-gradient(135deg,#c8fff0,#b8d9ff,#e5caff,#fff0c9);
 color:white;
}

body{
 padding:12px 8px 24px;
 background:
 radial-gradient(ellipse at 10% 5%,#70f5cf88,transparent 38%),
 radial-gradient(ellipse at 90% 15%,#8a9dff88,transparent 35%),
 radial-gradient(ellipse at 50% 100%,#ffcf7a66,transparent 42%),
 linear-gradient(135deg,#d7fff1,#d9e7ff 52%,#f1ddff);
}

.phone{
 width:100%;max-width:440px;min-height:820px;
 margin:0 auto;padding:10px;border-radius:38px;
 background:linear-gradient(145deg,#e5fff7,#8be7d3 24%,#92aaff 58%,#d6a9ff 82%,#ffe0a0);
 box-shadow:0 25px 65px #344e7960,inset 0 0 0 2px #ffffffb0;
}

.screen{
 min-height:800px;overflow:hidden;position:relative;
 border-radius:30px;padding:18px 15px 24px;
 background:
 radial-gradient(circle at 5% 0%,#35e9bd55,transparent 35%),
 radial-gradient(circle at 100% 30%,#826bff55,transparent 38%),
 linear-gradient(145deg,#153d49,#173c50 45%,#292c5a 100