import datetime
import streamlit as st
from info_gathering import ask_for_info, filter_response
from personal_details import PersonalDetails

st.title("HULE: Bot that sells")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.user_details = PersonalDetails()
    question = ask_for_info()
    st.session_state.messages.append({"role": "assistant", "content": question})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    st.write("reacting on input ", datetime.datetime.now())
    with st.chat_message("user"):
        st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    
    user = st.session_state.user_details
    user, ask_for = filter_response(user_input, user)
    st.session_state.user_details = user
    st.write(user)
    
    if ask_for:
        question = ask_for_info(ask_for)
        st.session_state.messages.append({"role": "assistant", "content": question})
        with st.chat_message("assistant"):
            st.markdown(question)
    else:
        with st.chat_message("assistant"):
            st.markdown("Thank you for your time. Have a great day!")