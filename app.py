import streamlit as st
from ui.pos_ui import pos_screen
from ui.admin_dashboard import admin_dashboard

st.set_page_config(page_title="All-in-One POS & Admin", layout="wide")

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["POS", "Admin Dashboard"])

if app_mode == "POS":
    pos_screen()
else:
    admin_dashboard()
