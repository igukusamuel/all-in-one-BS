import streamlit as st
from core.inventory import get_inventory
from core.config import VAT_RATE, LOW_STOCK_THRESHOLD
from core.shift import record_cash_sale
from services.pos_service import process_sale

def pos_screen():

    st.title("Point of Sale")

    # --- Ensure shift is open ---
    if "shift" not in st.session_state or not st.session_state.shift["is_open"]:
        st.warning("Shift not open.")
        return

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    products = get_inventory()
    categories = sorted(set(p["category"] for p in products))
    selected_category = st.sidebar.selectbox("Category", categories)

    filtered = [p for p in products if p["category"] == selected_category]

    st.subheader("Products")

    cols = st.columns(4)

    for i, product in enumerate(filtered):
        with cols[i % 4]:

            low_stock = product["stock"] <= LOW_STOCK_THRESHOLD
            badge = " 🔴 LOW" if low_stock else ""

            st.markdown(f"**{product['name']}{badge}**")
            st.write(f"Stock: {product['stock']}")
            st.write(f"Price: {product['price']}")

            if st.button(f"Add {product['name']}", key=f"add_{product['name']}"):

                current = st.session_state.cart.get(product["name"], 0)

                if current + 1 > product["stock"]:
                    st.warning("Cannot exceed stock")
                else:
                    st.session_state.cart[product["name"]] = current + 1
                    st.rerun()

    st.divider()
    st.subheader("Cart")

    subtotal = 0

    for name, qty in list(st.session_state.cart.items()):
        price = next(p["price"] for p in products if p["name"] == name)
        subtotal += price * qty

        col1, col2, col3, col4 = st.columns([3,1,1,1])

        with col1:
            st.write(name)

        with col2:
            st.write(qty)

        with col3:
            if st.button("+", key=f"plus_{name}"):
                stock = next(p["stock"] for p in products if p["name"] == name)
                if qty + 1 <= stock:
                    st.session_state.cart[name] += 1
                    st.rerun()

        with col4:
            if st.button("-", key=f"minus_{name}"):
                if qty - 1 <= 0:
                    del st.session_state.cart[name]
                else:
                    st.session_state.cart[name] -= 1
                st.rerun()

    tax = round(subtotal * VAT_RATE)
    total = round(subtotal + tax)

    st.write(f"Subtotal: {round(subtotal)}")
    st.write(f"Tax: {tax}")
    st.write(f"**Total: {total}**")

    payment_method = st.radio("Payment Method", ["Cash", "Card", "Mobile Wallet"])

    amount_received = 0

    if payment_method == "Cash":
        amount_received = st.number_input("Cash Received", min_value=0.0)
        change = round(amount_received - total)
        if amount_received >= total:
            st.success(f"Change Due: {change}")
        else:
            st.error("Insufficient cash")

    if st.button("Complete Sale"):

        if payment_method == "Cash" and amount_received < total:
            st.stop()

        process_sale(st.session_state.cart, total, payment_method)

        if payment_method == "Cash":
            record_cash_sale(st.session_state.shift, total)

        st.session_state.cart = {}
        st.success("Sale Completed")
        st.rerun()
