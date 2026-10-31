
import streamlit as st
from google import genai

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NEXORA AI")
st.caption("Your Intelligent AI Assistant")

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception:
    st.error("AI connection setup issue. Check your API key in Streamlit Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("NEXORA")
    st.write("Your personal AI assistant.")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                answer = response.text or "I couldn't generate a response."
            except Exception:
                answer = "Sorry, something went wrong. Please check your API quota and connection."

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
