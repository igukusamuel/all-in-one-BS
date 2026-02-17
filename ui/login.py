import streamlit as st

def login_screen():
    st.title("Retail OS - Login")

    username = st.text_input("Username")
    if st.button("Login"):
        if username:
            st.session_state.user = username
            st.rerun()

