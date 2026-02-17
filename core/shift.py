import streamlit as st
import datetime

def open_shift(float_amount):
    st.session_state.shift = {
        "shift_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "float": float_amount,
        "cash_sales": 0,
        "cash_counted": 0
    }
