
import streamlit as st
import time
import io
import base64
import hashlib
import tempfile
import os

from groq import Groq
from pypdf import PdfReader
from PIL import Image

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NEXORA AI")
st.caption("Your Intelligent AI Assistant")

# Connect Groq
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("AI Connection Failed")
    st.code(f"{type(e).__name__}: {e}")
    st.stop()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_prompt" not in st.session_state:
    st.session_state.voice_prompt = ""

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = ""

# Sidebar
with st.sidebar:
    st.title("NEXORA")
    st.write("Your personal AI assistant.")

    voice_output = st.toggle(
        "🔊 Voice replies (English)",
        value=False
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.voice_prompt = ""
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image and PDF uploads
st.subheader("📎 Attachments")

image_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "webp"],
    key="image_upload"
)

pdf_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    key="pdf_upload"
)

# Voice input
st.subheader("🎤 Voice Input")

audio_file = st.audio_input("Record your message")

if audio_file is not None:
    audio_bytes = audio_file.getvalue()
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    if audio_hash != st.session_state.last_audio_hash:
        try:
            with st.spinner("Transcribing your voice..."):
                transcription = client.audio.transcriptions.create(
                    file=(
                        "recording.wav",
                        audio_bytes
                    ),
                    model="whisper-large-v3-turbo"
                )

                st.session_state.voice_prompt = transcription.text
                st.session_state.last_audio_hash = audio_hash

        except Exception as e:
            st.error("Voice transcription failed.")
            st.code(f"{type(e).__name__}: {e}")

if st.session_state.voice_prompt:
    st.info("Voice transcription: " + st.session_state.voice_prompt)

# Text input
prompt = st.chat_input("Ask NEXORA anything...")

if not prompt and st.session_state.voice_prompt:
    prompt = st.session_state.voice_prompt
    st.session_state.voice_prompt = ""

# Process request
if prompt:

    user_message = prompt

    # Read PDF
    pdf_text = ""

    if pdf_file is not None:
        try:
            reader = PdfReader(io.BytesIO(pdf_file.getvalue()))

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    pdf_text += extracted + "\n"

            if not pdf_text.strip():
                st.warning(
                    "No selectable text found in PDF. "
                    "Scanned PDFs need OCR."
                )

            else:
                user_message += (
                    "\n\nPDF DOCUMENT CONTENT:\n"
                    + pdf_text[:30000]
                )

        except Exception as e:
            st.error("PDF reading failed.")
            st.code(str(e))

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(prompt)

        if image_file is not None:
            st.image(image_file, width=250)

        if pdf_file is not None:
            st.caption("📄 PDF attached: " + pdf_file.name)

    # Prepare conversation
    history = [
        {
            "role": "system",
            "content": (
                "You are NEXORA AI, a helpful, intelligent "
                "and friendly AI assistant. Give accurate, "
                "clear and useful answers. Maintain conversation context."
            )
        }
    ]

    history += [
        {
            "role": m["role"],
            "content": m["content"]
        }
        for m in st.session_state.messages[:-1]
    ]

    # Prepare current message
    if image_file is not None:
        try:
            image = Image.open(image_file).convert("RGB")
            image.thumbnail((1600, 1600))

            image_buffer = io.BytesIO()
            image.save(image_buffer, format="JPEG", quality=85)

            image_base64 = base64.b64encode(
                image_buffer.getvalue()
            ).decode("utf-8")

            current_content = [
                {
                    "type": "text",
                    "text": user_message
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": (
                            "data:image/jpeg;base64,"
                            + image_base64
                        )
                    }
                }
            ]

            history.append({
                "role": "user",
                "content": current_content
            })

            selected_model = "qwen/qwen3.8-27b"

        except Exception as e:
            st.error("Image processing failed.")
            st.code(str(e))
            history.append({
                "role": "user",
                "content": user_message
            })
            selected_model = "openai/gpt-oss-120b"

    else:
        history.append({
            "role": "user",
            "content": user_message
        })
        selected_model = "openai/gpt-oss-120b"

    # Generate answer
    with st.chat_message("assistant"):
        answer = None

        for attempt in range(3):
            try:
                with st.spinner("NEXORA is thinking..."):
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=history
                    )

                answer = response.choices[0].message.content
                break

            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** (attempt + 1))
                else:
                    answer = (
                        f"API Error: {type(e).__name__}\n\n"
                        f"Details: {e}"
                    )

        st.markdown(answer)

        # Voice output
        if voice_output and answer and not answer.startswith("API Error:"):
            try:
                speech_text = answer[:200]

                with st.spinner("Generating voice..."):
                    speech = client.audio.speech.create(
                        model="canopylabs/orpheus-v1-english",
                        voice="autumn",
                        input=speech_text,
                        response_format="wav"
                    )

                    with tempfile.NamedTemporaryFile(
                        suffix=".wav",
                        delete=False
                    ) as temp_audio:
                        audio_path = temp_audio.name

                    speech.write_to_file(audio_path)

                    with open(audio_path, "rb") as audio:
                        st.audio(audio.read(), format="audio/wav")

                    os.remove(audio_path)

            except Exception as e:
                st.warning(
                    "Voice output unavailable. "
                    "It currently supports English speech."
                )

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
