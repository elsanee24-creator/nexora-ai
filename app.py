
import streamlit as st
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
        with st.spinner("NEXORA is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                answer = response.text or "No response was generated."

            except Exception as e:
                answer = (
                    f"API Error: {type(e).__name__}\n\n"
                    f"Details: {e}"
                )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    
