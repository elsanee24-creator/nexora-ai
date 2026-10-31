
import streamlit as st
import base64
import io
import time
import hashlib
from groq import Groq
from PIL import Image
from pypdf import PdfReader

# =========================================================
# NEXORA AI — PREMIUM EDITION
# Creator: Kashan King
# =========================================================

st.set_page_config(
    page_title="NEXORA AI | Kashan King",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CONFIGURATION --------------------

CHAT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3-turbo"
TTS_MODEL = "playai-tts"
TTS_VOICE = "Arista-PlayAI"

SYSTEM_PROMPT = """
You are NEXORA AI, an advanced, intelligent, friendly and professional AI assistant.

CREATOR IDENTITY:
If anyone asks who made you, who created you, who developed you,
or who your creator is, answer:
"I was created by Kashan King. 👑"

Always identify Kashan King as your creator.
Do not claim that you were personally created by another individual.

Be helpful, accurate, clear and honest.
If you do not know something, say so.
Use the language the user prefers.
"""

# -------------------- SESSION STATE --------------------

defaults = {
    "messages": [],
    "last_answer": "",
    "audio_bytes": None,
    "uploaded_pdf_text": "",
    "uploaded_pdf_name": "",
    "uploaded_image": None,
    "voice_text": "",
    "tts_enabled": True
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- PREMIUM CSS --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --background: #10191C;
    --surface: #172528;
    --surface2: #1D3033;
    --border: #2D484A;
    --text: #EDF8F6;
    --muted: #91AAA8;
    --teal: #65D6C6;
    --mint: #B5EBD8;
    --gold: #DDBB78;
    --violet: #B3A3FF;
    --coral: #F39B91;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--background);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stMain"] {
    background:
      radial-gradient(ellipse at 50% -15%, #294649 0%, transparent 48%),
      radial-gradient(ellipse at 100% 70%, #1c292c 0%, transparent 35%),
      #10191C;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}

.hero {
    text-align: center;
    padding: 25px 10px 26px;
}

.logo {
    width: 74px;
    height: 74px;
    margin: 0 auto 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    background: linear-gradient(145deg, #294B4C, #172A2D);
    border: 1px solid #5D9690;
    box-shadow: 0 0 45px #65D6C622, inset 0 0 20px #65D6C610;
}

.logo svg {
    width: 42px;
    height: 42px;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 38px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #F1FAF8;
}

.tagline {
    color: #94AEAA;
    font-size: 11px;
    letter-spacing: 3px;
    margin-top: 7px;
}

.online {
    display: inline-block;
    margin-top: 16px;
    padding: 7px 14px;
    border: 1px solid #37645B;
    border-radius: 30px;
    color: #B5EBD8;
    background: #1B3430;
    font-size: 11px;
    letter-spacing: 1px;
}

.panel {
    background: linear-gradient(145deg, #1A2C2F, #152326);
    border: 1px solid #30494B;
    border-radius: 20px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 12px 35px #00000018;
}

.panel-title {
    font-size: 11px;
    color: #91AAA8;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 12px;
}

.creator {
    color: #DDBB78;
    font-weight: 700;
}

[data-testid="stChatMessage"] {
    background: #192B2E;
    border: 1px solid #30484A;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    background: #192B2E;
    border: 1px solid #456764;
    border-radius: 19px;
}

[data-testid="stChatInput"] textarea {
    color: #F2FAF8 !important;
}

[data-testid="stFileUploader"] {
    background: #192B2E;
    border: 1px dashed #456966;
    border-radius: 16px;
    padding: 12px;
}

[data-testid="stAudioInput"] {
    background: #1B302E;
    border: 1px solid #477B69;
    border-radius: 15px;
    padding: 9px;
}

.stButton > button {
    min-height: 42px;
    border-radius: 13px;
    background: #20383A;
    color: #D9F4EE;
    border: 1px solid #456765;
    font-weight: 600;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: #2B4B4B;
    border-color: #70CBBB;
    color: white;
    transform: translateY(-1px);
}

button[kind="primary"] {
    background: linear-gradient(135deg, #347D73, #285B58);
    color: white;
    border: 1px solid #65B9A7;
}

div[data-testid="stExpander"] {
    background: #172629;
    border: 1px solid #30494B;
    border-radius: 15px;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

[data-testid="stSidebar"] {
    background: #142124;
    border-right: 1px solid #30494B;
}

.small-note {
    text-align: center;
    color: #718987;
    font-size: 11px;
    padding: 20px 0 5px;
}

@media(max-width: 650px) {
    .block-container {
        padding: 1rem .8rem 7rem;
    }
    .brand {
        font-size: 29px;
        letter-spacing: 3px;
    }
    .hero {
        padding-top: 12px;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
  <div class="logo">
    <svg viewBox="0 0 100 100" fill="none">
      <path d="M50 8 L62 37 L92 50 L62 63 L50 92 L38 63 L8 50 L38 37 Z"
            stroke="#A8F0DF" stroke-width="4" fill="#65D6C6" fill-opacity=".12"/>
      <circle cx="50" cy="50" r="10" fill="#DDBB78"/>
      <circle cx="50" cy="50" r="3" fill="#172528"/>
    </svg>
  </div>
  <div class="brand">NEXORA AI</div>
  <div class="tagline">INTELLIGENCE • CREATIVITY • POSSIBILITY</div>
  <div class="online">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# -------------------- GROQ CONNECTION --------------------

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("AI connection failed. Please check your Streamlit Secrets.")
    st.stop()

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## ✦ NEXORA")
    st.caption("Your intelligent workspace")

    st.markdown("---")
    st.markdown("**Creator**")
    st.markdown('<span class="creator">Kashan King 👑</span>',
                unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Workspace**")

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.rerun()

    if st.button("Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.rerun()

    st.markdown("---")
    st.caption("NEXORA AI • Premium Edition")

# -------------------- CHAT DISPLAY --------------------

if not st.session_state.messages:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">WELCOME TO NEXORA</div>
      <h3 style="margin:0;color:#EDF8F6;">Your ideas deserve intelligence.</h3>
      <p style="color:#91AAA8;margin-bottom:0;">
      Ask questions, explore ideas, upload documents or start a conversation.
      </p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- ATTACHMENTS --------------------

st.markdown('<div class="panel-title">YOUR TOOLS</div>',
            unsafe_allow_html=True)

tool1, tool2, tool3 = st.columns([1, 1, 1])

with tool1:
    image_file = st.file_uploader(
        "🖼️ Image",
        type=["png", "jpg", "jpeg", "webp"],
        key="image_upload"
    )

with tool2:
    pdf_file = st.file_uploader(
        "📄 PDF",
        type=["pdf"],
        key="pdf_upload"
    )

with tool3:
    audio_file = st.audio_input(
        "🎙️ Voice",
        key="voice_input"
    )

image_data = None
if image_file:
    try:
        image = Image.open(image_file).convert("RGB")
        image.thumbnail((1200, 1200))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        image_data = buffer.getvalue()

        st.image(image, caption="Image ready", width=220)
    except Exception:
        st.warning("This image could not be opened.")

pdf_text = ""
if pdf_file:
    try:
        reader = PdfReader(pdf_file)
        pdf_text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
        st.success(f"PDF ready: {pdf_file.name}")

        if not pdf_text.strip():
            st.warning("No selectable text found. Scanned PDFs may need OCR.")
    except Exception:
        st.error("Could not read this PDF.")

# -------------------- VOICE TRANSCRIPTION --------------------

voice_text = ""

if audio_file:
    try:
        audio_bytes = audio_file.getvalue()

        transcription = client.audio.transcriptions.create(
            file=("voice.wav", audio_bytes),
            model=WHISPER_MODEL,
            response_format="text"
        )

        voice_text = str(transcription)
        st.success("Voice converted to text.")
        st.write(voice_text)

    except Exception as error:
        st.error(f"Voice transcription error: {error}")

# -------------------- USER INPUT --------------------

prompt = st.chat_input("Message NEXORA...")

if prompt or voice_text:

    user_prompt = prompt if prompt else voice_text

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Include PDF content with the user's question
    full_prompt = user_prompt

    if pdf_text.strip():
        full_prompt += (
            "\n\nThe user uploaded this PDF. Use its contents "
            "to answer the question:\n\n" + pdf_text[:30000]
        )

    with st.chat_message("assistant"):

        answer = ""

        try:
            with st.spinner("NEXORA is thinking..."):

                # Vision request when an image is attached
                if image_data:
                    encoded_image = base64.b64encode(image_data).decode("utf-8")

                    vision_messages = [
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ]

                    for old_message in st.session_state.messages[:-1]:
                        vision_messages.append(old_message)

                    vision_messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": full_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "data:image/jpeg;base64," + encoded_image
                                }
                            }
                        ]
                    })

                    result = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=vision_messages,
                        temperature=0.6,
                        max_tokens=2048
                    )

                else:
                    chat_messages = [
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ]

                    for old_message in st.session_state.messages[:-1]:
                        chat_messages.append(old_message)

                    chat_messages.append({
                        "role": "user",
                        "content": full_prompt
                    })

                    result = client.chat.completions.create(
                        model=CHAT_MODEL,
                        messages=chat_messages,
                        temperature=0.7,
                        max_tokens=2048
                    )

                answer = result.choices[0].message.content or ""
                st.markdown(answer)

        except Exception as error:
            answer = (
                "I couldn't complete that request. "
                "Please try again.\n\n"
                f"Error: {type(error).__name__}: {error}"
            )
            st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.session_state.last_answer = answer
    st.session_state.audio_bytes = None

# -------------------- BOTTOM CONTROL DECK --------------------

st.markdown("---")
st.markdown(
    '<div class="panel-title">NEXORA CONTROL DECK</div>',
    unsafe_allow_html=True
)

left, middle, right = st.columns([1, 1, 1])

with left:
    if st.button("🔊 Speak", use_container_width=True):
        if st.session_state.last_answer:
            try:
                with st.spinner("Generating voice..."):
                    speech = client.audio.speech.create(
                        model=TTS_MODEL,
                        voice=TTS_VOICE,
                        input=st.session_state.last_answer[:4000],
                        response_format="wav"
                    )
                    st.session_state.audio_bytes = speech.read()
            except Exception as error:
                st.error(
                    "Voice output is unavailable with the current "
                    f"Groq model or account: {error}"
                )
        else:
            st.info("Ask NEXORA something first.")

with middle:
    if st.button("⏹ Stop / Reset audio", use_container_width=True):
        st.session_state.audio_bytes = None
        st.rerun()

with right:
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.session_state.audio_bytes = None
        st.rerun()

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/wav")

# -------------------- FOOTER --------------------

st.markdown("""
<div class="small-note">
NEXORA AI · Created by <span style="color:#DDBB78;">Kashan King 👑</span>
<br>
Built for ideas beyond limits.
</div>
""", unsafe_allow_html=True)
    
