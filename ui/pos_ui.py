import streamlit as st
from core.inventory import get_inventory, reduce_inventory
from core.accounting import post_sale
from ui.close_shift_ui import close_shift_screen


def pos_screen():

    # ----------------------------------
    # INIT STATE
    # ----------------------------------
    if "cart" not in st.session_state:
        st.session_state.cart = []

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "pos"  # pos or close_shift

    # ----------------------------------
    # ROUTING
    # ----------------------------------
    if st.session_state.view_mode == "close_shift":
        close_shift_screen()
        return

    # ----------------------------------
    # POS SCREEN
    # ----------------------------------
    st.title("Point of Sale")

    inventory = get_inventory()

    col1, col2 = st.columns([2, 1])

    # ----------------------------------
    # PRODUCTS PANEL
    # ----------------------------------
    with col1:
        st.subheader("Products")

        for item in inventory:
            if item["stock"] > 0:
                if st.button(
                    f"{item['name']} | ${item['price']} | Stock: {item['stock']}"
                ):
                    st.session_state.cart.append(item)

    # ----------------------------------
    # CART PANEL
    # ----------------------------------
    with col2:
        st.subheader("Cart")

        total = 0

        for index, item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])

            with col_a:
                st.write(f"{item['name']} - ${item['price']}")

            with col_b:
                if st.button("❌", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()

            total += item["price"]

        st.divider()
        st.write(f"**Total: ${total}**")

        # -------------------------------
        # PAYMENT
        # -------------------------------
        if st.button("Pay (Cash)", use_container_width=True):

            if len(st.session_state.cart) == 0:
                st.warning("Cart is empty.")
                return

            for item in st.session_state.cart:
                reduce_inventory(item["name"], 1)

            post_sale(total)

            st.session_state.shift["cash_sales"] += total
            st.session_state.cart = []

            st.success("Sale Completed")

        st.divider()

        # -------------------------------
        # CLOSE SHIFT BUTTON
        # -------------------------------
        if st.button("Close Shift", use_container_width=True):
            st.session_state.view_mode = "close_shift"
            st.rerun()
