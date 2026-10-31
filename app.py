
import streamlit as st
import io
import base64
from groq import Groq
from PIL import Image
from pypdf import PdfReader

# ==================================================
# NEXORA AI — CLEAN PREMIUM INTERFACE
# Created by Kashan King
# ==================================================

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="✦",
    layout="wide"
)

CHAT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3-turbo"

SYSTEM_PROMPT = """
You are NEXORA AI, an intelligent and helpful AI assistant.

If someone asks who created, made, developed or owns you,
answer: I was created by Kashan King. 👑

Always identify Kashan King as your creator.
Be accurate, friendly, professional and honest.
Respond in the language used by the user.
"""

# ---------------- STATE ----------------

for key, default in {
    "messages": [],
    "image_data": None,
    "pdf_text": "",
    "voice_text": "",
    "last_answer": "",
    "audio_data": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #10151F;
    --panel: #1A2433;
    --panel2: #202D3D;
    --border: #35465B;
    --text: #F2F5FC;
    --muted: #B2C0D2;
    --teal: #63D9CE;
    --gold: #E9C47A;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stMain"] {
    background:
        radial-gradient(ellipse at 50% 0%, #263D50 0%, transparent 48%),
        #10151F;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 900px;
    padding: 1.2rem 1rem 7rem;
}

.hero {
    text-align: center;
    padding: 20px 0 28px;
}

.logo {
    width: 65px;
    height: 65px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto auto 14px;
    background: linear-gradient(145deg, #294C5D, #1B2B3B);
    border: 1px solid #598C99;
    box-shadow: 0 0 35px #63D9CE20;
    color: #B8F4E8;
    font-size: 32px;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 34px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
}

.subtitle {
    color: #B2C0D2;
    font-size: 11px;
    letter-spacing: 3px;
    margin-top: 6px;
}

.status {
    display: inline-block;
    color: #B8F4D9;
    background: #1D3937;
    border: 1px solid #46766F;
    border-radius: 30px;
    padding: 6px 13px;
    margin-top: 14px;
    font-size: 11px;
}

[data-testid="stChatMessage"] {
    background: #1A2939;
    border: 1px solid #344A60;
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #F2F5FC !important;
}

[data-testid="stChatInput"] {
    background: #202E40 !important;
    border: 1px solid #66808F !important;
    border-radius: 18px !important;
}

[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #B6C5D6 !important;
}

.stButton > button {
    background: #223448;
    color: #F1F6FC;
    border: 1px solid #50677C;
    border-radius: 14px;
    min-height: 40px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #304B5D;
    border-color: #73CFC6;
    color: white;
}

div[data-testid="stPopover"] > button {
    width: 48px;
    height: 48px;
    min-height: 48px;
    border-radius: 50%;
    background: #26394C;
    color: white;
    border: 1px solid #60798B;
    font-size: 20px;
}

div[data-testid="stPopover"] > button:hover {
    background: #35566A;
    border-color: #75D8CE;
}

[data-testid="stPopoverBody"] {
    background: #1B2939;
    border: 1px solid #425B70;
    border-radius: 16px;
}

[data-testid="stFileUploader"] {
    background: #202F40;
    border: 1px dashed #6D8998;
    border-radius: 13px;
    padding: 8px;
}

[data-testid="stFileUploader"] label,
[data-testid="stAudioInput"] label {
    color: #F1F6FC !important;
}

[data-testid="stAudioInput"] {
    background: #203A3B;
    border: 1px solid #548B80;
    border-radius: 14px;
    padding: 8px;
}

[data-testid="stExpander"] {
    background: #1A2939;
    border: 1px solid #40566B;
    border-radius: 14px;
}

[data-testid="stMarkdownContainer"] p {
    color: #E8EFF8;
}

.creator {
    color: #E9C47A;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #A8B7C8;
    font-size: 11px;
    padding: 22px 0;
}

@media(max-width: 600px) {
    .block-container {
        padding: 1rem .75rem 6rem;
    }
    .brand {
        font-size: 29px;
    }
    .hero {
        padding-top: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="logo">✦</div>
    <div class="brand">NEXORA AI</div>
    <div class="subtitle">INTELLIGENCE • CREATIVITY • POSSIBILITY</div>
    <div class="status">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ---------------- API ----------------

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Connection failed. Check your Streamlit Secrets.")
    st.stop()

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ✦ NEXORA AI")
    st.caption("Your intelligent workspace")

    st.markdown("### Creator")
    st.markdown(
        '<span class="creator">Kashan King 👑</span>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.session_state.image_data = None
        st.session_state.pdf_text = ""
        st.session_state.audio_data = None
        st.rerun()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.rerun()

# ---------------- CHAT HISTORY ----------------

if not st.session_state.messages:
    st.markdown("""
    <div style="
        background:linear-gradient(145deg,#1C3040,#1A2939);
        border:1px solid #40566B;
        border-radius:18px;
        padding:22px;
        margin-bottom:20px;">
        <div style="color:#79DCD0;font-size:11px;letter-spacing:2px;">
        YOUR AI WORKSPACE
        </div>
        <h3 style="color:white;margin-bottom:5px;">
        Welcome to NEXORA.
        </h3>
        <p style="color:#C0CDDB;margin:0;">
        Ask anything. Explore ideas. Make something extraordinary.
        </p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- COMPACT TOOLBAR ----------------

st.markdown(
    '<p style="color:#AFC0D1;font-size:11px;letter-spacing:2px;">QUICK TOOLS</p>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    with st.popover("🖼️"):
        st.caption("IMAGE UPLOAD")
        image_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="image_file"
        )

        if image_file:
            try:
                img = Image.open(image_file).convert("RGB")
                img.thumbnail((1200, 1200))
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                st.session_state.image_data = buffer.getvalue()
                st.image(img, use_container_width=True)
                st.success("Image attached")
            except Exception:
                st.error("Could not open image.")

with c2:
    with st.popover("📄"):
        st.caption("PDF READER")
        pdf_file = st.file_uploader(
            "Choose a PDF",
            type=["pdf"],
            key="pdf_file"
        )

        if pdf_file:
            try:
                reader = PdfReader(pdf_file)
                st.session_state.pdf_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )[:30000]
                st.success("PDF attached")
            except Exception:
                st.error("Could not read PDF.")

with c3:
    with st.popover("🎙️"):
        st.caption("VOICE INPUT")
        audio_file = st.audio_input(
            "Record your message",
            key="audio_file"
        )

        if audio_file:
            if st.button("Convert voice to text"):
                try:
                    transcription = client.audio.transcriptions.create(
                        file=("voice.wav", audio_file.getvalue()),
                        model=WHISPER_MODEL,
                        response_format="text"
                    )
                    st.session_state.voice_text = str(transcription)
                    st.success("Voice converted")
                    st.write(st.session_state.voice_text)
                except Exception as e:
                    st.error(f"Voice error: {e}")

with c4:
    if st.button("🔊", help="Play last answer"):
        if st.session_state.last_answer:
            try:
                speech = client.audio.speech.create(
                    model="playai-tts",
                    voice="Arista-PlayAI",
                    input=st.session_state.last_answer[:4000],
                    response_format="wav"
                )
                st.session_state.audio_data = speech.read()
            except Exception as e:
                st.error(f"Voice output unavailable: {e}")
        else:
            st.info("Ask NEXORA something first.")

with c5:
    if st.button("⏹", help="Stop/reset audio"):
        st.session_state.audio_data = None
        st.rerun()

with c6:
    if st.button("＋", help="New chat"):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.session_state.image_data = None
        st.session_state.pdf_text = ""
        st.session_state.audio_data = None
        st.rerun()

if st.session_state.audio_data:
    st.audio(st.session_state.audio_data, format="audio/wav")

# ---------------- INPUT ----------------

prompt = st.chat_input("Message NEXORA...")

if not prompt and st.session_state.voice_text:
    prompt = st.session_state.voice_text
    st.session_state.voice_text = ""

# ---------------- AI RESPONSE ----------------

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = prompt

    if st.session_state.pdf_text:
        full_prompt += (
            "\n\nUse this uploaded PDF as reference:\n"
            + st.session_state.pdf_text
        )

    try:
        with st.chat_message("assistant"):
            with st.spinner("NEXORA is thinking..."):

                history = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + st.session_state.messages[:-1]

                if st.session_state.image_data:
                    encoded = base64.b64encode(
                        st.session_state.image_data
                    ).decode("utf-8")

                    vision_history = history + [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": full_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "data:image/jpeg;base64," + encoded
                                }
                            }
                        ]
                    }]

                    result = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=vision_history,
                        max_tokens=2048
                    )

                else:
                    history.append({
                        "role": "user",
                        "content": full_prompt
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

        # Clear attachments after successful response
        st.session_state.image_data = None
        st.session_state.pdf_text = ""

    except Exception as e:
        st.error(f"AI Error: {type(e).__name__}: {e}")

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    NEXORA AI · Created by
    <span class="creator">Kashan King 👑</span>
    <br><br>
    Intelligence without limits.
</div>
""", unsafe_allow_html=True)
