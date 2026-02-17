import streamlit as st
from ui.login_ui import login_screen
from ui.pos_ui import pos_screen
from ui.admin_ui import admin_screen
from ui.shift_ui import shift_controls
from ui.ledger_ui import ledger_screen

st.set_page_config(layout="wide")

if "user" not in st.session_state:
    login_screen()
else:

    role = st.session_state.user["role"]

    shift_controls()

    menu = ["POS", "Ledger"]

    if role == "admin":
        menu.append("Admin")

    choice = st.sidebar.radio("Menu", menu)

    if choice == "POS":
        pos_screen()
    elif choice == "Admin" and role == "admin":
        admin_screen()
    elif choice == "Ledger":
        ledger_screen()
