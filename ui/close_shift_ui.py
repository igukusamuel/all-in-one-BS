import streamlit as st

def close_shift_screen():
    st.title("Close Shift")

    expected = st.session_state.shift["float"] + st.session_state.shift["cash_sales"]
    counted = st.number_input("Counted Cash", min_value=0.0)

    variance = counted - expected

    st.write("Expected:", expected)
    st.write("Variance:", variance)

    if st.button("Confirm Close"):
        st.session_state.shift_open = False
        st.success("Shift Closed")
        st.rerun()
