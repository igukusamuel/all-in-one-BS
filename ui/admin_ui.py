import streamlit as st
from services.reorder_service import check_auto_reorder
from core.inventory import get_inventory

def admin_screen():

    st.title("Admin Dashboard")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.subheader("Low Stock")

    low = check_auto_reorder()
    cols = st.columns(4)

    for i, p in enumerate(low):
        with cols[i % 4]:
            st.write(p["name"])
            st.write(f"Stock: {p['stock']}")
            st.button(f"Order {p['name']}")
