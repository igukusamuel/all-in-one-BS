import streamlit as st
from core.inventory import get_inventory, reduce_inventory
from core.accounting import post_sale

def pos_screen():
    st.title("POS")

    if "cart" not in st.session_state:
        st.session_state.cart = []

    inventory = get_inventory()

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("Products")
        for item in inventory:
            if st.button(f"{item['name']} (${item['price']})"):
                st.session_state.cart.append(item)

    with col2:
        st.subheader("Cart")

        total = 0
        for item in st.session_state.cart:
            st.write(item["name"], item["price"])
            total += item["price"]

        st.write("Total:", total)

        if st.button("Pay (Cash)"):
            for item in st.session_state.cart:
                reduce_inventory(item["name"], 1)
            post_sale(total)
            st.session_state.shift["cash_sales"] += total
            st.session_state.cart = []
            st.success("Sale Completed")

