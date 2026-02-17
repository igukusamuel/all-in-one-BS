import streamlit as st
from ui.pos_ui import pos_screen
from ui.admin_dashboard import admin_dashboard

st.set_page_config(page_title="All-in-One POS System", layout="wide")

# -------------------------
# SESSION INIT
# -------------------------
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# -------------------------
# LOGIN SCREEN
# -------------------------
if st.session_state.user_role is None:
    st.title("Store Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        role = st.selectbox("Role", ["cashier", "admin"])
        submit = st.form_submit_button("Login")

        if submit and username:
            st.session_state.username = username
            st.session_state.user_role = role
            st.success(f"Logged in as {role}")
            st.rerun()

    st.stop()

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.write(f"Logged in as: {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.user_role = None
    st.rerun()

if st.session_state.user_role == "admin":
    app_mode = st.sidebar.radio("Navigation", ["POS", "Admin Dashboard"])
else:
    app_mode = "POS"  # Cashier sees only POS

if app_mode == "POS":
    pos_screen()
else:
    admin_dashboard()
