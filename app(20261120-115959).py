import streamlit as st
import base64
import io

from groq import Groq
from PIL import Image
from pypdf import PdfReader

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
"I was created by Mustafa King. 👑"

Always identify Kashan King as your creator.
Be accurate, friendly and professional.
Respond in the user's language.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "login_name" not in st.session_state:
    st.session_state.login_name = ""


# -------------------- GLOBAL DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Kaushan+Script&display=swap');

:root {
    --bg: #101722;
    --user: #29465C;
    --assistant: #202D3D;
    --text: #F5F7FC;
    --muted: #B7C5D5;
    --accent: #77D9CD;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stMain"] {
    background:
      radial-gradient(ellipse at 50% 0%, #263D51 0%, transparent 48%),
      #101722;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 850px;
    padding-top: 1rem;
    padding-bottom: 6rem;
}

/* -------------------- LOGIN SCREEN -------------------- */

.login-shell {
    position: relative;
    min-height: 88vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    isolation: isolate;
    border-radius: 28px;
    background:
        radial-gradient(ellipse at 50% 100%, rgba(255, 73, 20, .30), transparent 48%),
        radial-gradient(ellipse at 15% 75%, rgba(255, 145, 35, .19), transparent 35%),
        radial-gradient(ellipse at 85% 70%, rgba(255, 35, 65, .18), transparent 38%),
        linear-gradient(160deg, #090d19 0%, #17101c 48%, #090e19 100%);
}

.login-shell::before,
.login-shell::after {
    content: "";
    position: absolute;
    z-index: -1;
    width: 75%;
    height: 75%;
    left: 12%;
    bottom: -48%;
    border-radius: 50%;
    filter: blur(48px);
    opacity: .65;
    background: linear-gradient(90deg, #ff4b1f, #ff9a2f, #ff315d, #ff4b1f);
    animation: flameRise 7s ease-in-out infinite alternate;
}

.login-shell::after {
    width: 55%;
    height: 65%;
    left: 25%;
    bottom: -42%;
    opacity: .45;
    filter: blur(65px);
    animation: flameRise 5s ease-in-out infinite alternate-reverse;
}

@keyframes flameRise {
    0% { transform: translate3d(-7%, 8%, 0) scale(.92) rotate(-5deg); }
    50% { transform: translate3d(5%, -9%, 0) scale(1.12) rotate(5deg); }
    100% { transform: translate3d(-3%, -17%, 0) scale(1.04) rotate(-3deg); }
}

.login-orb {
    position: absolute;
    z-index: -1;
    border-radius: 50%;
    pointer-events: none;
    filter: blur(2px);
    background: radial-gradient(circle, rgba(255, 194, 117, .95) 0%, rgba(255, 94, 45, .45) 28%, transparent 70%);
    animation: floatParticle linear infinite;
}

.p1 { width: 13px; height: 13px; left: 8%; bottom: 8%; animation-duration: 9s; }
.p2 { width: 8px; height: 8px; left: 20%; bottom: 2%; animation-duration: 12s; animation-delay: -4s; }
.p3 { width: 11px; height: 11px; left: 35%; bottom: 5%; animation-duration: 10s; animation-delay: -2s; }
.p4 { width: 7px; height: 7px; left: 50%; bottom: 1%; animation-duration: 13s; animation-delay: -7s; }
.p5 { width: 12px; height: 12px; left: 66%; bottom: 6%; animation-duration: 11s; animation-delay: -3s; }
.p6 { width: 8px; height: 8px; left: 82%; bottom: 3%; animation-duration: 14s; animation-delay: -8s; }
.p7 { width: 10px; height: 10px; left: 92%; bottom: 9%; animation-duration: 10s; animation-delay: -5s; }
.p8 { width: 6px; height: 6px; left: 14%; bottom: 20%; animation-duration: 15s; animation-delay: -6s; }
.p9 { width: 9px; height: 9px; left: 74%; bottom: 16%; animation-duration: 12s; animation-delay: -1s; }
.p10 { width: 7px; height: 7px; left: 43%; bottom: 12%; animation-duration: 16s; animation-delay: -9s; }

@keyframes floatParticle {
    0% { transform: translate3d(0, 0, 0) scale(.6); opacity: 0; }
    12% { opacity: .9; }
    75% { opacity: .65; }
    100% { transform: translate3d(28px, -620px, 0) scale(1.25); opacity: 0; }
}

.login-content {
    position: relative;
    z-index: 2;
    width: min(440px, 90%);
    margin: 38px auto;
    padding: 35px 30px 30px;
    border: 1px solid rgba(255, 190, 150, .28);
    border-radius: 27px;
    background: linear-gradient(145deg, rgba(28, 29, 43, .82), rgba(17, 21, 34, .78));
    box-shadow: 0 25px 80px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.10);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    text-align: center;
}

.login-mark {
    width: 58px;
    height: 58px;
    margin: 0 auto 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 19px;
    color: #ffe1c0;
    font-size: 29px;
    background: linear-gradient(145deg, rgba(255,117,57,.35), rgba(255,54,92,.17));
    border: 1px solid rgba(255,174,124,.48);
    box-shadow: 0 0 30px rgba(255,95,50,.22);
}

.login-brand {
    font-family: 'Kaushan Script', cursive;
    font-size: clamp(35px, 7vw, 49px);
    line-height: 1.25;
    font-weight: 400;
    letter-spacing: 1px;
    background: linear-gradient(100deg, #ffe0a8 5%, #ff9a70 42%, #ff6b9b 72%, #b8a4ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    filter: drop-shadow(0 0 17px rgba(255,116,112,.24));
}

.login-tagline {
    margin-top: 9px;
    margin-bottom: 24px;
    color: #c8c5d7;
    font-size: 10px;
    letter-spacing: 3px;
}

.login-note {
    color: #c8c8d5;
    font-size: 13px;
    margin-bottom: 20px;
}

.login-content label {
    color: #f0eaf0 !important;
}

.login-content [data-testid="stTextInput"] input {
    background: rgba(12, 17, 29, .78) !important;
    color: #fff !important;
    border: 1px solid rgba(255, 174, 145, .30) !important;
    border-radius: 12px !important;
}

.login-content [data-testid="stTextInput"] input:focus {
    border-color: #ff9b83 !important;
    box-shadow: 0 0 0 1px #ff9b83 !important;
}

.login-content [data-testid="stFormSubmitButton"] button {
    width: 100%;
    min-height: 47px;
    border: 1px solid rgba(255,190,160,.48);
    border-radius: 13px;
    color: #211522;
    font-weight: 800;
    background: linear-gradient(100deg, #ffd49a, #ff9679, #ff7e9e);
    transition: transform .2s ease, filter .2s ease;
}

.login-content [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
}

.login-small {
    color: #aaaabd;
    font-size: 11px;
    margin-top: 18px;
}

.login-footer {
    color: rgba(238,220,224,.70);
    font-size: 11px;
    letter-spacing: .5px;
    text-align: center;
    padding: 0 0 20px;
}

/* -------------------- CHAT DESIGN -------------------- */

.hero {
    text-align: center;
    padding: 18px 0 28px;
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
    color: #B7C5D5;
    font-size: 10px;
    letter-spacing: 3px;
    margin-top: 6px;
}

[data-testid="stChatMessage"] {
    border-radius: 19px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #42566B;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #202D3D;
    border-color: #42566B;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #29465C;
    border-color: #52738B;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong {
    color: #F5F7FC !important;
}

[data-testid="stChatInput"] {
    background: #202D3D !important;
    border: 1px solid #66899A !important;
    border-radius: 20px !important;
}

[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
    caret-color: #77D9CD !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #C2CEDB !important;
}

[data-testid="stChatInput"] button {
    color: #D8F5ED !important;
}

[data-testid="stSidebar"] {
    background: #172333;
    border-right: 1px solid #344B60;
}

.stButton > button {
    background: #263B50;
    color: white;
    border: 1px solid #536D82;
    border-radius: 12px;
    min-height: 40px;
}

.stButton > button:hover {
    background: #35566B;
    border-color: #77D9CD;
    color: white;
}

.footer {
    text-align: center;
    color: #B7C5D5;
    font-size: 11px;
    padding: 22px 0;
}

@media(max-width:600px) {
    .block-container {
        padding: .8rem .7rem 6rem;
    }
    .login-shell {
        min-height: 82vh;
        border-radius: 20px;
    }
    .login-content {
        padding: 29px 20px 25px;
    }
    .brand {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- LOGIN GATE --------------------

if not st.session_state.authenticated:

    st.markdown("""
    <div class="login-shell">
        <div class="login-orb p1"></div>
        <div class="login-orb p2"></div>
        <div class="login-orb p3"></div>
        <div class="login-orb p4"></div>
        <div class="login-orb p5"></div>
        <div class="login-orb p6"></div>
        <div class="login-orb p7"></div>
        <div class="login-orb p8"></div>
        <div class="login-orb p9"></div>
        <div class="login-orb p10"></div>
        <div class="login-content">
            <div class="login-mark">✦</div>
            <div class="login-brand">KASHAN'S AI</div>
            <div class="login-tagline">YOUR INTELLIGENT AI EXPERIENCE</div>
            <div class="login-note">Welcome back. Sign in to continue.</div>
    """, unsafe_allow_html=True)

    with st.form("kashan_login_form"):
        login_name = st.text_input("Username", placeholder="Enter your username")
        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        submitted = st.form_submit_button("SIGN IN  →", use_container_width=True)

    st.markdown("""
            <div class="login-small">A smarter space for ideas, answers and creativity.</div>
        </div>
    </div>
    <div class="login-footer">KASHAN'S AI · Created by Kashan King 👑</div>
    """, unsafe_allow_html=True)

    if submitted:
        if login_name.strip() and login_password:
            # Temporary UI-only login gate.
            # Real account verification will be added when credentials/authentication are defined.
            st.session_state.authenticated = True
            st.session_state.login_name = login_name.strip()
            st.rerun()
        else:
            st.error("Please enter both username and password.")

    st.stop()


# -------------------- CHAT HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="logo">✦</div>
    <div class="brand">KASHAN'S AI</div>
    <div class="subtitle">YOUR INTELLIGENT AI ASSISTANT</div>
</div>
""", unsafe_allow_html=True)


# -------------------- CONNECTION --------------------

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("AI connection failed. Check Streamlit Secrets.")
    st.stop()


# -------------------- SIDEBAR --------------------

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

    if st.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.login_name = ""
        st.rerun()


# -------------------- CHAT HISTORY --------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------- CHAT INPUT --------------------

submission = st.chat_input(
    "Message KASHAN'S AI...",
    accept_file="multiple",
    file_type=["png", "jpg", "jpeg", "webp", "pdf"],
    accept_audio=True,
    audio_sample_rate=16000,
    max_upload_size=20,
    key="nexora_chat"
)


# -------------------- PROCESS SUBMISSION --------------------

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


# -------------------- FOOTER --------------------

st.markdown("""
<div class="footer">
    KASHAN'S AI · Created by
    <span style="color:#E9C47A;">Kashan King 👑</span>
</div>
""", unsafe_allow_html=True)
