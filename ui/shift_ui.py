import streamlit as st
from core.shift import open_shift

def shift_open_screen():
    st.title("Open Shift")

    float_amount = st.number_input("Enter Opening Float", min_value=0.0)

    if st.button("Start Shift"):
        open_shift(float_amount)
        st.session_state.shift_open = True
        st.rerun()

