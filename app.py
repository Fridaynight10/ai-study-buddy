import streamlit as st

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("📚 AI Study Buddy")
st.caption("Ask me anything you're studying!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_reply(history):
    # TODO: call your LLM API here and return the reply text
    return "API not connected yet. Replace this function with a real API call."

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What do you want to learn today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = get_ai_reply(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
