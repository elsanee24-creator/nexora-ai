
import streamlit as st
import time
from groq import Groq

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

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("NEXORA")
    st.write("Your personal AI assistant.")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask NEXORA anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = None

        for attempt in range(3):
            try:
                with st.spinner("NEXORA is thinking..."):
                    chat = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are NEXORA AI, a helpful and intelligent AI assistant."
                            }
                        ] + st.session_state.messages
                    )

                answer = chat.choices[0].message.content
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

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    
