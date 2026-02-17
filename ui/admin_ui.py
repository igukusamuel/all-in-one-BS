import streamlit as st
from services.reorder_service import check_auto_reorder
from core.inventory import get_inventory

def admin_screen():

    st.title("Admin Dashboard")

    low_stock = check_auto_reorder()

    st.subheader("Low Stock Items")

    cols = st.columns(4)

    for i, product in enumerate(low_stock):
        with cols[i % 4]:
            st.markdown(f"### {product['name']}")
            st.write(f"Stock: {product['stock']}")
            st.button(f"Order {product['name']}")

