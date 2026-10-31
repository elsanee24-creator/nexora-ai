
import streamlit as st
import base64
import io

from groq import Groq
from PIL import Image
from pypdf import PdfReader

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="✦",
    layout="wide"
)

CHAT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
WHISPER_MODEL = "whisper-large-v3-turbo"

SYSTEM_PROMPT = """
You are NEXORA AI, a helpful and advanced AI assistant.

If asked who made, created or developed you, answer:
"I was created by Kashan King. 👑"

Always identify Kashan King as your creator.
Be accurate, friendly and professional.
Respond in the user's language.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

# -------------------- PREMIUM DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

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

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #202D3D;
    border-color: #42566B;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #29465C;
    border-color: #52738B;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong {
    color: #F5F7FC !important;
}

/* Input */
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

/* Attachment and audio controls */
[data-testid="stChatInput"] button {
    color: #D8F5ED !important;
}

/* Sidebar */
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
    .brand {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="logo">✦</div>
    <div class="brand">NEXORA AI</div>
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
    st.markdown("## ✦ NEXORA AI")
    st.caption("Your personal AI assistant")

    st.markdown("**Created by Kashan King 👑**")

    st.divider()

    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.rerun()

    if st.button("Clear history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_answer = ""
        st.rerun()

# -------------------- CHAT HISTORY --------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- CHAT INPUT --------------------

submission = st.chat_input(
    "Message NEXORA...",
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
            with st.spinner("NEXORA is thinking..."):

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
    NEXORA AI · Created by
    <span style="color:#E9C47A;">Kashan King 👑</span>
</div>
""", unsafe_allow_html=True)
