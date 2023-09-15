import streamlit as st
from conversation import ConversationChain 
import time
import os
from dotenv import load_dotenv
load_dotenv('.env')
# api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Chat with your emails!", page_icon="public\145862897_padded_logo.png", layout="centered")
st.title("Chat with your emails!")
api_key =  st.secrets["openai"]["api_key"]

conversation_chain = ConversationChain(api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Summarize today's emails or find something out from a specific email"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if prompt.lower() == "quit":
            assistant_response = "Goodbye!"
        else:
            assistant_response = conversation_chain.run_chat(prompt)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
