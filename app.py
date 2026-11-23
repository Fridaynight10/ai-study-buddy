import time
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("📚 AI Study Buddy")
st.caption("Ask me anything you're studying!")

# Reads from Streamlit Secrets when deployed online, or falls back to your local key
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_reply(history):
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    config = types.GenerateContentConfig(
        system_instruction="You are a helpful AI Study Buddy. Give clear explanations, step-by-step help, summaries, and practice quiz questions when asked."
    )

    models = ["gemini-3.5-flash-lite", "gemini-4-hydrogen", "gemini-3.8-flash"]
    for attempt in range(2):
        for model_name in models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                return response.text
            except Exception as e:
                if "503" in str(e) or "404" in str(e):
                    continue
                return f"Error: {e}"
        time.sleep(2)
    return "Google's AI servers are busy right now—please send your message again in a few seconds."
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What do you want to learn today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        reply = get_ai_reply(st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
