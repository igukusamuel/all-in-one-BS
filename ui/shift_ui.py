import streamlit as st
from core.shift import open_shift, close_shift

def shift_controls():

    st.sidebar.subheader("Shift")

    if "shift" not in st.session_state:
        st.session_state.shift = {"is_open": False}

    if not st.session_state.shift["is_open"]:
        amount = st.sidebar.number_input("Beginning Cash", min_value=0.0)
        if st.sidebar.button("Open Shift"):
            st.session_state.shift = open_shift(amount)
            st.sidebar.success("Shift Opened")
            st.rerun()
    else:
        st.sidebar.success("Shift Open")

        actual_cash = st.sidebar.number_input("Actual Cash Count", min_value=0.0)
        if st.sidebar.button("Close Shift"):
            expected, variance = close_shift(st.session_state.shift, actual_cash)
            st.sidebar.write(f"Expected: {expected}")
            st.sidebar.write(f"Variance: {variance}")
