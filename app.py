import streamlit as st
import base64
import io
import time
import json
import re

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

CHAT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3-turbo"

SYSTEM_PROMPT = """
You are KASHAN'S AI, a helpful and advanced AI assistant.

If asked who made, created or developed you, answer:
"I was created by Kashan King. 👑"

Always identify Kashan King as your creator.
Be accurate, friendly and professional.
Respond in the user's language.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "login_name" not in st.session_state:
    st.session_state.login_name = ""

if "current_page" not in st.session_state:
    st.session_state.current_page = "login"


# ============================================================
# GLOBAL STYLE SYSTEM
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Kaushan+Script&display=swap');

:root {
    --page-bg: #17243a;
    --text-main: #f5f7fc;
    --muted-text: #b9c8dc;
    --accent: #83e6df;
    --login-ink: #20243b;
    --login-field: #f2efff;
    --chat-field: #ffffff;
    --chat-ink: #18263b;
}

html, body, [data-testid="stAppViewContainer"] {
    min-height: 100%;
    background: var(--page-bg);
    color: var(--text-main);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMain"] {
    background:
        radial-gradient(ellipse at 12% 12%, rgba(77, 115, 170, .34), transparent 37%),
        radial-gradient(ellipse at 88% 85%, rgba(98, 79, 163, .27), transparent 42%),
        linear-gradient(135deg, #17243a 0%, #202d49 48%, #17243a 100%);
    background-size: 150% 150%;
    animation: pageAtmosphere 18s ease-in-out infinite alternate;
}

@keyframes pageAtmosphere {
    0% { background-position: 0% 20%; }
    100% { background-position: 100% 80%; }
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 980px;
    padding-top: 0.8rem;
    padding-bottom: 2rem;
}

/* ============================================================
   LOGIN STAGE - FLAMES AND FLOATING EMBERS
   ============================================================ */

.st-key-login_stage {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    width: 100%;
    min-height: calc(100vh - 2rem);
    box-sizing: border-box;
    border-radius: 28px;
    padding: 22px 18px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(ellipse at 50% 100%, rgba(255, 73, 20, .30), transparent 48%),
        radial-gradient(ellipse at 15% 75%, rgba(255, 145, 35, .19), transparent 35%),
        radial-gradient(ellipse at 85% 70%, rgba(255, 35, 65, .18), transparent 38%),
        linear-gradient(160deg, #090d19 0%, #17101c 48%, #090e19 100%);
}

.st-key-login_stage::before,
.st-key-login_stage::after {
    content: "";
    position: absolute;
    z-index: 0;
    width: 78%;
    height: 70%;
    left: 11%;
    bottom: -47%;
    border-radius: 50%;
    filter: blur(48px);
    opacity: .68;
    background: linear-gradient(90deg, #ff4b1f, #ff9a2f, #ff315d, #ff4b1f);
    animation: loginFlameRise 7s ease-in-out infinite alternate;
    pointer-events: none;
}

.st-key-login_stage::after {
    width: 58%;
    height: 60%;
    left: 21%;
    bottom: -43%;
    opacity: .46;
    filter: blur(68px);
    animation: loginFlameRise 5s ease-in-out infinite alternate-reverse;
}

@keyframes loginFlameRise {
    0% { transform: translate3d(-7%, 8%, 0) scale(.92) rotate(-5deg); }
    50% { transform: translate3d(5%, -9%, 0) scale(1.12) rotate(5deg); }
    100% { transform: translate3d(-3%, -17%, 0) scale(1.04) rotate(-3deg); }
}

.login-flame {
    position: absolute;
    bottom: -12%;
    display: block;
    width: clamp(54px, 10vw, 125px);
    height: clamp(180px, 38vh, 390px);
    transform-origin: 50% 100%;
    border-radius: 58% 42% 48% 52% / 72% 70% 30% 28%;
    background:
        radial-gradient(ellipse at 50% 76%, #fff5bd 0 5%, #ffd45e 16%, #ff8a2b 38%, #f04422 62%, rgba(174,24,35,.08) 78%, transparent 82%);
    filter: drop-shadow(0 0 18px rgba(255, 105, 30, .45));
    opacity: .78;
    animation: flameDance 3.8s ease-in-out infinite alternate;
    pointer-events: none;
}
.login-flame:nth-of-type(1) { left: 3%; height: 34vh; animation-delay: -.8s; }
.login-flame:nth-of-type(2) { left: 14%; height: 48vh; width: clamp(65px, 12vw, 145px); animation-delay: -2.1s; }
.login-flame:nth-of-type(3) { left: 29%; height: 39vh; animation-delay: -1.4s; }
.login-flame:nth-of-type(4) { left: 43%; height: 54vh; width: clamp(70px, 13vw, 155px); animation-delay: -2.8s; }
.login-flame:nth-of-type(5) { right: 29%; height: 43vh; animation-delay: -.5s; }
.login-flame:nth-of-type(6) { right: 14%; height: 50vh; width: clamp(65px, 12vw, 145px); animation-delay: -1.8s; }
.login-flame:nth-of-type(7) { right: 3%; height: 35vh; animation-delay: -2.4s; }

@keyframes flameDance {
    0% { transform: translate3d(-8px, 0, 0) rotate(-7deg) scaleX(.82) scaleY(.88); opacity: .48; }
    35% { transform: translate3d(7px, -24px, 0) rotate(5deg) scaleX(1.08) scaleY(1.06); opacity: .82; }
    70% { transform: translate3d(-5px, -11px, 0) rotate(-4deg) scaleX(.94) scaleY(1.12); opacity: .66; }
    100% { transform: translate3d(9px, -32px, 0) rotate(8deg) scaleX(1.12) scaleY(.98); opacity: .9; }
}

.login-particles {
    position: absolute;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}

.login-particle {
    position: absolute;
    bottom: -25px;
    display: block;
    border-radius: 50%;
    background: radial-gradient(circle, #fff0c9 0%, #ff9b51 38%, rgba(255, 80, 40, 0) 75%);
    box-shadow: 0 0 15px rgba(255, 139, 74, .75);
    animation: emberTravel linear infinite;
}

.login-particle:nth-child(1) { left: 5%; width: 9px; height: 9px; animation-duration: 10s; }
.login-particle:nth-child(2) { left: 13%; width: 6px; height: 6px; animation-duration: 13s; animation-delay: -4s; }
.login-particle:nth-child(3) { left: 22%; width: 11px; height: 11px; animation-duration: 11s; animation-delay: -2s; }
.login-particle:nth-child(4) { left: 31%; width: 7px; height: 7px; animation-duration: 14s; animation-delay: -8s; }
.login-particle:nth-child(5) { left: 40%; width: 5px; height: 5px; animation-duration: 12s; animation-delay: -5s; }
.login-particle:nth-child(6) { left: 49%; width: 10px; height: 10px; animation-duration: 15s; animation-delay: -1s; }
.login-particle:nth-child(7) { left: 58%; width: 6px; height: 6px; animation-duration: 11s; animation-delay: -7s; }
.login-particle:nth-child(8) { left: 67%; width: 8px; height: 8px; animation-duration: 13s; animation-delay: -3s; }
.login-particle:nth-child(9) { left: 76%; width: 5px; height: 5px; animation-duration: 16s; animation-delay: -9s; }
.login-particle:nth-child(10) { left: 85%; width: 9px; height: 9px; animation-duration: 12s; animation-delay: -6s; }
.login-particle:nth-child(11) { left: 94%; width: 7px; height: 7px; animation-duration: 14s; animation-delay: -2s; }

@keyframes emberTravel {
    0% { transform: translate3d(0, 0, 0) scale(.55); opacity: 0; }
    12% { opacity: .9; }
    75% { opacity: .65; }
    100% { transform: translate3d(35px, -680px, 0) scale(1.2); opacity: 0; }
}

.st-key-login_card {
    position: relative;
    z-index: 2;
    width: min(440px, 100%);
    max-width: 440px;
    margin: 0 auto;
    padding: 27px 30px 24px;
    box-sizing: border-box;
    border: 1px solid rgba(255, 190, 150, .30);
    border-radius: 27px;
    background: linear-gradient(145deg, rgba(28, 29, 43, .88), rgba(17, 21, 34, .86));
    box-shadow: 0 25px 80px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.10);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

.login-mark {
    width: 54px;
    height: 54px;
    margin: 0 auto 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    color: #ffe1c0;
    font-size: 28px;
    background: linear-gradient(145deg, rgba(255,117,57,.35), rgba(255,54,92,.17));
    border: 1px solid rgba(255,174,124,.48);
    box-shadow: 0 0 30px rgba(255,95,50,.22);
}

.login-brand {
    font-family: 'Kaushan Script', cursive;
    font-size: clamp(35px, 7vw, 49px);
    line-height: 1.22;
    font-weight: 400;
    letter-spacing: 1px;
    text-align: center;
    background: linear-gradient(100deg, #ffe0a8 5%, #ff9a70 42%, #ff6b9b 72%, #b8a4ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    filter: drop-shadow(0 0 17px rgba(255,116,112,.24));
}

.login-tagline {
    margin-top: 8px;
    margin-bottom: 17px;
    color: #d2cddd;
    font-size: 10px;
    letter-spacing: 2.5px;
    text-align: center;
}

.login-note {
    color: #d4d1df;
    font-size: 13px;
    text-align: center;
    margin-bottom: 14px;
}

.st-key-login_card label {
    color: #f0eaf0 !important;
}

.st-key-login_card [data-testid="stTextInput"] input {
    background: var(--login-field) !important;
    color: var(--login-ink) !important;
    -webkit-text-fill-color: var(--login-ink) !important;
    caret-color: #8b3d70 !important;
    border: 1px solid rgba(255, 174, 145, .55) !important;
    border-radius: 12px !important;
}

.st-key-login_card [data-testid="stTextInput"] input::placeholder {
    color: #6c6880 !important;
    -webkit-text-fill-color: #6c6880 !important;
    opacity: 1 !important;
}

.st-key-login_card [data-testid="stTextInput"] input:focus {
    border-color: #ff9b83 !important;
    box-shadow: 0 0 0 1px #ff9b83 !important;
}

.st-key-login_card [data-testid="stFormSubmitButton"] button {
    width: 100%;
    min-height: 47px;
    border: 1px solid rgba(255,190,160,.48);
    border-radius: 13px;
    color: #211522 !important;
    font-weight: 800;
    background: linear-gradient(100deg, #ffd49a, #ff9679, #ff7e9e);
    transition: transform .2s ease, filter .2s ease;
}

.st-key-login_card [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
}

.login-small {
    color: #bdb8cc;
    font-size: 11px;
    text-align: center;
    margin-top: 13px;
}

.login-footer {
    position: relative;
    z-index: 2;
    color: rgba(238,220,224,.76);
    font-size: 11px;
    letter-spacing: .5px;
    text-align: center;
    margin-top: 13px;
}

/* ============================================================
   HOME SCREEN - AURORA / COSMIC MOVEMENT
   ============================================================ */

.st-key-home_stage {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    width: 100%;
    min-height: calc(100vh - 2rem);
    box-sizing: border-box;
    border-radius: 28px;
    padding: 28px;
    background:
        radial-gradient(ellipse at 15% 20%, rgba(54, 211, 202, .24), transparent 38%),
        radial-gradient(ellipse at 82% 75%, rgba(134, 103, 255, .29), transparent 42%),
        linear-gradient(135deg, #142a42 0%, #203d5d 48%, #1d2345 100%);
}

.st-key-home_stage::before,
.st-key-home_stage::after {
    content: "";
    position: absolute;
    z-index: -1;
    width: 75%;
    height: 65%;
    border-radius: 50%;
    filter: blur(65px);
    opacity: .42;
    pointer-events: none;
}

.st-key-home_stage::before {
    left: -20%;
    top: -20%;
    background: linear-gradient(120deg, #39d6c7, #4d8bff, #8a6cff);
    animation: auroraDrift 14s ease-in-out infinite alternate;
}

.st-key-home_stage::after {
    right: -20%;
    bottom: -25%;
    background: linear-gradient(120deg, #7a69ff, #4bb6d5, #54e1c0);
    animation: auroraDrift 17s ease-in-out infinite alternate-reverse;
}

@keyframes auroraDrift {
    0% { transform: translate3d(-5%, 4%, 0) rotate(-8deg) scale(.92); }
    50% { transform: translate3d(9%, -6%, 0) rotate(8deg) scale(1.12); }
    100% { transform: translate3d(-2%, 9%, 0) rotate(-3deg) scale(1.04); }
}

.home-stars {
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    overflow: hidden;
}

.home-star {
    position: absolute;
    display: block;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #e3ffff;
    box-shadow: 0 0 12px 3px rgba(157, 241, 255, .45);
    animation: starFloat 9s ease-in-out infinite;
}

.home-star:nth-child(1) { left: 8%; top: 18%; animation-delay: -2s; }
.home-star:nth-child(2) { left: 19%; top: 72%; width: 3px; height: 3px; animation-delay: -5s; }
.home-star:nth-child(3) { left: 34%; top: 28%; animation-delay: -1s; }
.home-star:nth-child(4) { left: 48%; top: 82%; width: 5px; height: 5px; animation-delay: -7s; }
.home-star:nth-child(5) { left: 63%; top: 16%; width: 3px; height: 3px; animation-delay: -3s; }
.home-star:nth-child(6) { left: 78%; top: 61%; animation-delay: -6s; }
.home-star:nth-child(7) { left: 91%; top: 31%; width: 3px; height: 3px; animation-delay: -4s; }
.home-star:nth-child(8) { left: 55%; top: 45%; width: 3px; height: 3px; animation-delay: -8s; }
.home-star:nth-child(9) { left: 27%; top: 48%; width: 5px; height: 5px; animation-delay: -3s; }
.home-star:nth-child(10) { left: 86%; top: 84%; width: 3px; height: 3px; animation-delay: -1s; }

@keyframes starFloat {
    0%, 100% { transform: translate3d(0, 0, 0); opacity: .25; }
    50% { transform: translate3d(13px, -22px, 0); opacity: 1; }
}

.home-heading {
    color: #f4fbff;
    font-size: clamp(28px, 5vw, 42px);
    font-weight: 800;
    letter-spacing: 1px;
    text-align: center;
    margin-top: 10vh;
    text-shadow: 0 5px 25px rgba(0,0,0,.22);
}

.home-subheading {
    color: #d2e5f3;
    text-align: center;
    font-size: 13px;
    letter-spacing: 1.2px;
    margin-top: 9px;
    margin-bottom: 28px;
}

.home-welcome {
    color: #e5f3ff;
    text-align: center;
    font-size: 14px;
    margin-bottom: 24px;
}

/* Home Buttons in one line with different colors */
.st-key-open_ai_button button {
    width: 100% !important;
    min-height: 52px !important;
    border-radius: 14px !important;
    color: #0b1f36 !important;
    font-weight: 800 !important;
    border: 1px solid rgba(180, 255, 248, .8) !important;
    background: linear-gradient(105deg, #7bf1e8, #9ad2ff) !important;
    box-shadow: 0 8px 22px rgba(80, 200, 210, .25);
}

.st-key-home_extra_button button {
    width: 100% !important;
    min-height: 52px !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border: 1px solid rgba(220, 190, 255, .6) !important;
    background: linear-gradient(105deg, #8a6cff, #c36cff) !important;
    box-shadow: 0 8px 22px rgba(138, 108, 255, .25);
}

.st-key-home_logout button {
    color: #ffffff !important;
    background: linear-gradient(135deg, #d9233d, #a80f2b) !important;
    border: 1px solid rgba(255, 190, 200, .65) !important;
    border-radius: 13px !important;
    min-height: 46px !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 24px rgba(190, 20, 55, .28);
}
.st-key-home_logout { margin-top: clamp(80px, 18vh, 180px); }

/* ============================================================
   AI CHAT SCREEN - CLEAN WHITE SNOWFALL CANVAS & CONTRAST FIX
   ============================================================ */
[data-testid="stMain"]:has(.chat-snow-layer) {
    background: #f7fbff !important;
    background-image: none !important;
    animation: none !important;
}

.hero {
    text-align: center;
    padding: 8px 0 16px;
}

.logo {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    margin: auto auto 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(145deg,#315
