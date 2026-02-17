import streamlit as st
from ui.login import login_screen
from ui.shift_ui import shift_open_screen
from ui.pos_ui import pos_screen
from ui.close_shift_ui import close_shift_screen

st.set_page_config(layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

if "shift_open" not in st.session_state:
    st.session_state.shift_open = False

if st.session_state.user is None:
    login_screen()
elif not st.session_state.shift_open:
    shift_open_screen()
else:
    pos_screen()

