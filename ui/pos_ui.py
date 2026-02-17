import streamlit as st
from core.inventory import get_inventory
from services.pos_service import process_sale
from core.config import VAT_RATE, LOW_STOCK_THRESHOLD

def pos_screen():

    st.title("Point of Sale")

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    products = get_inventory()

    categories = list(set(p["category"] for p in products))
    selected_category = st.sidebar.selectbox("Category", categories)

    filtered = [p for p in products if p["category"] == selected_category]

    cols = st.columns(4)

    for i, product in enumerate(filtered):
        with cols[i % 4]:

            low_stock = product["stock"] <= LOW_STOCK_THRESHOLD

            badge = " 🔴 LOW" if low_stock else ""

            st.markdown(f"### {product['name']}{badge}")
            st.write(f"Stock: {product['stock']}")
            st.write(f"Price: {product['price']}")

            if st.button(f"Add {product['name']}"):
                current = st.session_state.cart.get(product["name"], 0)

                if current + 1 > product["stock"]:
                    st.warning("Insufficient stock")
                else:
                    st.session_state.cart[product["name"]] = current + 1
                    st.rerun()

    st.divider()

    subtotal = 0
    for name, qty in st.session_state.cart.items():
        price = next(p["price"] for p in products if p["name"] == name)
        subtotal += price * qty

    tax = round(subtotal * VAT_RATE, 0)
    total = round(subtotal + tax, 0)

    st.subheader("Cart")
    st.write(st.session_state.cart)
    st.write(f"Subtotal: {round(subtotal,0)}")
    st.write(f"Tax: {tax}")
    st.write(f"Total: {total}")

    payment_method = st.radio("Payment", ["Cash", "Card", "Mobile Wallet"])

    if payment_method == "Cash":
        amount = st.number_input("Amount Received", min_value=0.0)
        change = round(amount - total, 0)
        if amount >= total:
            st.success(f"Change: {change}")
        else:
            st.error("Insufficient cash")

    if st.button("Complete Sale"):

        if payment_method == "Cash" and amount < total:
            st.stop()

        process_sale(st.session_state.cart, total, payment_method)

        st.session_state.cart = {}
        st.success("Sale Completed")
        st.rerun()
