
import streamlit as st
import time
from google import genai

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NEXORA AI")
st.caption("Your Intelligent AI Assistant")

# Connect AI
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

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

# Display previous messages
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
                with st.spinner(
                    f"NEXORA is thinking... Attempt {attempt + 1}/3"
                ):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                answer = response.text or "No response was generated."
                break

            except Exception as e:
                error = str(e)

                if "503" in error or "UNAVAILABLE" in error:
                    if attempt < 2:
                        time.sleep(2 ** (attempt + 1))
                    else:
                        answer = (
                            "Gemini server is still busy. "
                            "Please try again in a few minutes."
                        )
                else:
                    answer = (
                        f"API Error: {type(e).__name__}\n\n"
                        f"Details: {e}"
                    )
                    break

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    
