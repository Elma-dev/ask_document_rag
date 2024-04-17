import streamlit as st
import random
import time


def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role):
        st.write(msg["msg"])
if prompt:=st.chat_input("your message"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "msg": prompt})
    with st.chat_message("assistant"):
        output=st.write_stream(response_generator())
    st.session_state.messages.append({"role": "assistant", "msg": output})

with st.container():
    st.file_uploader("",type="pdf")