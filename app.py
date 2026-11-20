import streamlit as st
import base64
import io
import time

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
    --chat-field: #e8f0fb;
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
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* ============================================================
   LOGIN STAGE - FLAMES AND FLOATING EMBERS
   ============================================================ */

.st-key-login_stage {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    width: 100%;
    min-height: calc(100vh - 2.5rem);
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


/* Layered flame tongues create a more visible 3D fire effect */
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

/* Decorative ember layer */
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

/* Actual Streamlit login card container */
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

/* Login inputs: light field + dark typed text */
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
   HOME SCREEN - AURORA / COSMIC MOVEMENT (NO FIRE)
   ============================================================ */

.st-key-home_stage {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    width: 100%;
    min-height: calc(100vh - 2.5rem);
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
    margin-top: 7vh;
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

.st-key-open_ai_button button,
.st-key-home_logout button,
.st-key-chat_home_button button {
    border-radius: 12px !important;
    min-height: 45px !important;
    font-weight: 700 !important;
}

.st-key-open_ai_button button {
    min-width: 225px !important;
    min-height: 54px !important;
    padding: 0 22px !important;
    border-radius: 13px !important;
    color: #14263d !important;
    border: 1px solid rgba(205,255,255,.75) !important;
    background: linear-gradient(105deg, #a9f4ed, #b7d9ff, #d4c4ff) !important;
    box-shadow: 0 9px 28px rgba(93, 208, 219, .20);
}

.st-key-open_ai_button button:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

.st-key-home_logout button,
.st-key-chat_home_button button {
    color: #eef7ff !important;
    background: rgba(20, 38, 62, .50) !important;
    border: 1px solid rgba(204, 232, 255, .30) !important;
}

/* ============================================================
   AI CHAT SCREEN - LIGHTER BLUE / PURPLE ATMOSPHERE
   ============================================================ */

[data-testid="stMain"] {
    background:
        radial-gradient(ellipse at 8% 12%, rgba(65, 132, 181, .30), transparent 38%),
        radial-gradient(ellipse at 90% 82%, rgba(120, 100, 191, .25), transparent 42%),
        linear-gradient(135deg, #182c45 0%, #263d5a 52%, #252b4b 100%);
    background-size: 170% 170%;
    animation: chatAurora 20s ease-in-out infinite alternate;
}

@keyframes chatAurora {
    0% { background-position: 0% 30%; }
    100% { background-position: 100% 70%; }
}

.hero {
    text-align: center;
    padding: 12px 0 24px;
}

.logo {
    width: 58px;
    height: 58px;
    border-radius: 19px;
    margin: auto auto 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(145deg,#31576C,#1A2C40);
    border: 1px solid #6D9DA9;
    color: #B8F3E8;
    font-size: 29px;
    box-shadow: 0 0 30px #77D9CD20;
}

.brand {
    color: white;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 4px;
}

.subtitle {
    color: #D0DFEF;
    font-size: 10px;
    letter-spacing: 3px;
    margin-top: 6px;
}

/* Chat message cards */
[data-testid="stChatMessage"] {
    border-radius: 19px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(177, 211, 239, .34);
    box-shadow: 0 8px 25px rgba(4, 15, 31, .12);
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(34, 54, 79, .91);
    border-color: rgba(151, 190, 220, .38);
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(47, 76, 105, .94);
    border-color: rgba(164, 204, 231, .42);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] span {
    color: #F5F8FF !important;
}

/* Chat input: pale field with dark text to avoid white-on-white */
[data-testid="stChatInput"] {
    background: var(--chat-field) !important;
    border: 1px solid #a9c3e0 !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(7, 19, 37, .18);
}

[data-testid="stChatInput"] textarea {
    color: var(--chat-ink) !important;
    -webkit-text-fill-color: var(--chat-ink) !important;
    caret-color: #315e94 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #596b82 !important;
    -webkit-text-fill-color: #596b82 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    color: #263e5b !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #172b43;
    border-right: 1px solid #405a76;
}

[data-testid="stSidebar"] * {
    color: #f1f6ff;
}

.stButton > button {
    background: #2b4562;
    color: white;
    border: 1px solid #66839f;
    border-radius: 12px;
    min-height: 40px;
}

.stButton > button:hover {
    background: #3a5c7c;
    border-color: #8bdedb;
    color: white;
}

.footer {
    text-align: center;
    color: #d0dfef;
    font-size: 11px;
    padding: 22px 0;
}


/* Arctic atmosphere for the AI chat page */
.chat-snow-layer {
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}
.chat-snowflake {
    position: absolute;
    top: -24px;
    display: block;
    width: var(--flake-size, 5px);
    height: var(--flake-size, 5px);
    border-radius: 50%;
    background: rgba(238, 250, 255, .92);
    box-shadow: 0 0 9px rgba(187, 231, 255, .72);
    opacity: var(--flake-opacity, .7);
    animation: snowFall var(--fall-duration, 12s) linear infinite;
    animation-delay: var(--fall-delay, 0s);
}
@keyframes snowFall {
    0% { transform: translate3d(0, -5vh, 0) rotate(0deg); }
    25% { transform: translate3d(24px, 25vh, 0) rotate(90deg); }
    50% { transform: translate3d(-18px, 52vh, 0) rotate(180deg); }
    75% { transform: translate3d(22px, 78vh, 0) rotate(270deg); }
    100% { transform: translate3d(-10px, 112vh, 0) rotate(360deg); }
}
[data-testid="stMain"]:has(.chat-snow-layer) .stMainBlockContainer {
    position: relative;
    z-index: 1;
}
@media (max-width: 600px) {
    .st-key-open_ai_button button {
        min-width: 0 !important;
        width: 100% !important;
        padding: 0 12px !important;
    }
}

/* Loading spinner appearance */
.stSpinner > div {
    border-top-color: #9cece5 !important;
}

/* Mobile layout */
@media (max-width: 600px) {
    .block-container {
        padding: .55rem .55rem 2rem;
    }

    .st-key-login_stage {
        min-height: calc(100svh - 1.5rem);
        border-radius: 20px;
        padding: 15px 10px;
    }

    .st-key-login_card {
        padding: 23px 18px 20px;
        border-radius: 22px;
    }

    .login-brand {
        font-size: 37px;
    }

    .st-key-home_stage {
        min-height: calc(100svh - 1.5rem);
        border-radius: 20px;
        padding: 15px;
    }

    .home-heading {
        margin-top: 10vh;
    }

    .brand {
        font-size: 27px;
    }

    [data-testid="stChatMessage"] {
        padding: 12px;
    }
}

@media (max-height: 700px) and (min-width: 601px) {
    .st-key-login_stage {
        min-height: calc(100vh - 2rem);
        padding-top: 12px;
        padding-bottom: 12px;
    }

    .st-key-login_card {
        padding-top: 19px;
        padding-bottom: 17px;
    }

    .login-mark {
        width: 46px;
        height: 46px;
        margin-bottom: 8px;
    }

    .login-tagline {
        margin-bottom: 10px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.authenticated:
    st.session_state.current_page = "login"

    with st.container(key="login_stage"):
        st.markdown("""
        <div class="login-particles">
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-flame"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
            <span class="login-particle"></span>
        </div>
        """, unsafe_allow_html=True)

        with st.container(key="login_card"):
            st.markdown("""
            <div class="login-mark">✦</div>
            <div class="login-brand">KASHAN'S AI</div>
            <div class="login-tagline">YOUR INTELLIGENT AI EXPERIENCE</div>
            <div class="login-note">Welcome back. Sign in to continue.</div>
            """, unsafe_allow_html=True)

            with st.form("kashan_login_form", clear_on_submit=False):
                login_name = st.text_input(
                    "Username",
                    placeholder="Enter your username"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                submitted = st.form_submit_button(
                    "SIGN IN  →",
                    use_container_width=True
                )

            st.markdown("""
            <div class="login-small">
                A smarter space for ideas, answers and creativity.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-footer">
            KASHAN'S AI · Created by Kashan King 👑
        </div>
        """, unsafe_allow_html=True)

    if submitted:
        if login_name.strip() and login_password:
            st.session_state.authenticated = True
            st.session_state.login_name = login_name.strip()
            st.session_state.current_page = "home"

            with st.spinner("Preparing your AI workspace..."):
                time.sleep(1)

            st.rerun()
        else:
            st.error("Please enter both username and password.")

    st.stop()


# ============================================================
# HOME / AI LAUNCHER PAGE
# ============================================================

if st.session_state.current_page == "home":
    with st.container(key="home_stage"):
        st.markdown("""
        <div class="home-stars">
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
            <span class="home-star"></span>
        </div>
        """, unsafe_allow_html=True)

        # AI Chat launcher: upper-left area, horizontal rectangle, with comfortable inset.
        launcher_column, empty_space = st.columns([1.35, 5.0])
        with launcher_column:
            if st.button(
                "✦  OPEN AI CHAT",
                key="open_ai_button",
                use_container_width=True
            ):
                st.session_state.current_page = "chat"
                with st.spinner("Opening KASHAN'S AI..."):
                    time.sleep(1)
                st.rerun()

        st.markdown("""
        <div class="home-heading">KASHAN'S AI</div>
        <div class="home-subheading">
            YOUR PERSONAL INTELLIGENCE SPACE
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="home-welcome">Welcome, {st.session_state.login_name}.</div>',
            unsafe_allow_html=True
        )

        logout_left, logout_center, logout_right = st.columns([1, 1.5, 1])
        with logout_center:
            if st.button(
                "Log out",
                key="home_logout",
                use_container_width=True
            ):
                st.session_state.authenticated = False
                st.session_state.login_name = ""
                st.session_state.current_page = "login"
                st.rerun()

    st.stop()


# ============================================================
# AI CHAT PAGE
# ============================================================

if st.session_state.current_page == "chat":

    st.markdown("""
    <div class="chat-snow-layer" aria-hidden="true">
        <span class="chat-snowflake" style="left:3%;--flake-size:4px;--fall-duration:12s;--fall-delay:-3s"></span>
        <span class="chat-snowflake" style="left:8%;--flake-size:7px;--fall-duration:16s;--fall-delay:-11s"></span>
        <span class="chat-snowflake" style="left:14%;--flake-size:3px;--fall-duration:10s;--fall-delay:-5s"></span>
        <span class="chat-snowflake" style="left:20%;--flake-size:6px;--fall-duration:14s;--fall-delay:-8s"></span>
        <span class="chat-snowflake" style="left:27%;--flake-size:4px;--fall-duration:11s;--fall-delay:-1s"></span>
        <span class="chat-snowflake" style="left:33%;--flake-size:8px;--fall-duration:18s;--fall-delay:-13s"></span>
        <span class="chat-snowflake" style="left:39%;--flake-size:3px;--fall-duration:13s;--fall-delay:-7s"></span>
        <span class="chat-snowflake" style="left:45%;--flake-size:5px;--fall-duration:15s;--fall-delay:-4s"></span>
        <span class="chat-snowflake" style="left:52%;--flake-size:4px;--fall-duration:12s;--fall-delay:-10s"></span>
        <span class="chat-snowflake" style="left:58%;--flake-size:7px;--fall-duration:17s;--fall-delay:-6s"></span>
        <span class="chat-snowflake" style="left:64%;--flake-size:3px;--fall-duration:11s;--fall-delay:-2s"></span>
        <span class="chat-snowflake" style="left:70%;--flake-size:6px;--fall-duration:15s;--fall-delay:-12s"></span>
        <span class="chat-snowflake" style="left:76%;--flake-size:4px;--fall-duration:13s;--fall-delay:-9s"></span>
        <span class="chat-snowflake" style="left:82%;--flake-size:8px;--fall-duration:19s;--fall-delay:-5s"></span>
        <span class="chat-snowflake" style="left:88%;--flake-size:3px;--fall-duration:10s;--fall-delay:-7s"></span>
        <span class="chat-snowflake" style="left:94%;--flake-size:5px;--fall-duration:14s;--fall-delay:-14s"></span>
        <span class="chat-snowflake" style="left:98%;--flake-size:4px;--fall-duration:16s;--fall-delay:-1s"></span>
    </div>
    """, unsafe_allow_html=True)

    top_left, top_space = st.columns([1, 5])

    with top_left:
        if st.button(
            "← Home",
            key="chat_home_button",
            use_container_width=True
        ):
            st.session_state.current_page = "home"
            st.rerun()

    st.markdown("""
    <div class="hero">
        <div class="logo">✦</div>
        <div class="brand">KASHAN'S AI</div>
        <div class="subtitle">YOUR INTELLIGENT AI ASSISTANT</div>
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # GROQ CONNECTION - ORIGINAL CONFIGURATION PRESERVED
    # --------------------------------------------------------

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        st.error("AI connection failed. Check Streamlit Secrets.")
        st.stop()


    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:
        st.markdown("## ✦ KASHAN'S AI")
        st.caption("Your personal AI assistant")
        st.markdown("**Created by Kashan King 👑**")
        st.caption(f"Signed in as: {st.session_state.login_name}")

        st.divider()

        if st.button("＋ New chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_answer = ""
            st.rerun()

        if st.button("Clear history", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_answer = ""
            st.rerun()

        st.divider()

        if st.button("Log out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.login_name = ""
            st.session_state.current_page = "login"
            st.rerun()


    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    # --------------------------------------------------------
    # CHAT INPUT - ORIGINAL OPTIONS PRESERVED
    # --------------------------------------------------------

    submission = st.chat_input(
        "Message KASHAN'S AI...",
        accept_file="multiple",
        file_type=["png", "jpg", "jpeg", "webp", "pdf"],
        accept_audio=True,
        audio_sample_rate=16000,
        max_upload_size=20,
        key="nexora_chat"
    )


    # --------------------------------------------------------
    # PROCESS SUBMISSION
    # --------------------------------------------------------

    if submission:

        user_text = submission.text or ""
        files = submission.files or []
        audio = submission.audio

        # Voice transcription
        if audio:
            try:
                transcript = client.audio.transcriptions.create(
                    file=("voice.wav", audio.getvalue()),
                    model=WHISPER_MODEL,
                    response_format="text"
                )
                user_text += "\n" + str(transcript)
            except Exception as e:
                st.error(f"Voice transcription failed: {e}")
                st.stop()

        image_parts = []
        pdf_parts = []

        # Process attachments
        for uploaded in files:

            file_name = uploaded.name.lower()

            if file_name.endswith(".pdf"):
                try:
                    reader = PdfReader(uploaded)
                    extracted = "\n".join(
                        page.extract_text() or ""
                        for page in reader.pages
                    )
                    pdf_parts.append(
                        f"PDF: {uploaded.name}\n{extracted[:25000]}"
                    )
                except Exception:
                    st.warning(f"Could not read {uploaded.name}")

            elif file_name.endswith((".png", ".jpg", ".jpeg", ".webp")):
                try:
                    image = Image.open(uploaded).convert("RGB")
                    image.thumbnail((1200, 1200))

                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG", quality=85)

                    encoded = base64.b64encode(
                        buffer.getvalue()
                    ).decode("utf-8")

                    image_parts.append(encoded)

                except Exception:
                    st.warning(f"Could not open {uploaded.name}")

        if pdf_parts:
            user_text += "\n\nUploaded document content:\n"
            user_text += "\n\n".join(pdf_parts)

        if not user_text.strip() and not image_parts:
            user_text = "Please analyze the attached file."

        # Display user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_text
        })

        with st.chat_message("user"):
            st.markdown(user_text or "Please analyze the attachment.")

            for encoded in image_parts:
                st.image(
                    base64.b64decode(encoded),
                    width=220
                )

            for uploaded in files:
                if uploaded.name.lower().endswith(".pdf"):
                    st.caption("📄 " + uploaded.name)

            if audio:
                st.caption("🎙️ Voice message received")

        # Generate answer
        try:
            with st.chat_message("assistant"):
                with st.spinner("KASHAN'S AI is thinking..."):

                    history = [
                        {"role": "system", "content": SYSTEM_PROMPT}
                    ]

                    history.extend(st.session_state.messages[:-1])

                    if image_parts:
                        content = [
                            {
                                "type": "text",
                                "text": user_text or "Describe this image."
                            }
                        ]

                        for encoded in image_parts:
                            content.append({
                                "type": "image_url",
                                "image_url": {
                                    "url": "data:image/jpeg;base64," + encoded
                                }
                            })

                        history.append({
                            "role": "user",
                            "content": content
                        })

                        result = client.chat.completions.create(
                            model=VISION_MODEL,
                            messages=history,
                            max_tokens=2048
                        )

                    else:
                        history.append({
                            "role": "user",
                            "content": user_text
                        })

                        result = client.chat.completions.create(
                            model=CHAT_MODEL,
                            messages=history,
                            temperature=0.7,
                            max_tokens=2048
                        )

                    answer = result.choices[0].message.content or ""
                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.session_state.last_answer = answer

        except Exception as e:
            st.error(f"AI Error: {type(e).__name__}: {e}")


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown("""
    <div class="footer">
        KASHAN'S AI · Created by
        <span style="color:#E9C47A;">Kashan King 👑</span>
    </div>
    """, unsafe_allow_html=True)
