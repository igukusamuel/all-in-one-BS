import streamlit as st

def get_staff():
    if "staff" not in st.session_state:
        st.session_state.staff = []
    return st.session_state.staff

def add_staff_member(name, role):
    if "staff" not in st.session_state:
        st.session_state.staff = []
    st.session_state.staff.append({"name": name, "role": role})
