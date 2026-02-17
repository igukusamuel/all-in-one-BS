import streamlit as st
from core.inventory import get_inventory, reduce_inventory, check_auto_reorder
from core.accounting import post_sale

CRITICAL_THRESHOLD = 10

def pos_screen():

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    inventory = get_inventory()

    st.title("Point of Sale")

    col_cat, col_products, col_cart = st.columns([1, 3, 1.5])

    # ---------------------
    # CATEGORY
    # ---------------------
    with col_cat:
        categories = sorted(set(i["category"] for i in inventory))
        selected_category = st.radio("Category", categories)

    # ---------------------
    # PRODUCT GRID (3x4)
    # ---------------------
    with col_products:
        filtered = [i for i in inventory if i["category"] == selected_category]
        cols_per_row = 3
        rows = (len(filtered) + cols_per_row - 1) // cols_per_row

        for r in range(rows):
            cols = st.columns(cols_per_row)
            for c in range(cols_per_row):
                idx = r * cols_per_row + c
                if idx < len(filtered):
                    item = filtered[idx]
                    with cols[c]:
                        st.markdown(f"### {item['name']}")
                        st.write(f"Price: ${item['price']}")
                        st.write(f"Stock: {item['stock']}")

                        if st.button("➕ Add", key=f"add_{item['name']}"):
                            if item["name"] in st.session_state.cart:
                                st.session_state.cart[item["name"]]["qty"] += 1
                            else:
                                st.session_state.cart[item["name"]] = {
                                    "price": item["price"],
                                    "qty": 1
                                }

    # ---------------------
    # CART
    # ---------------------
    with col_cart:
        st.subheader("Cart")
        subtotal = 0

        for name, data in list(st.session_state.cart.items()):
            col1, col2, col3 = st.columns([2,1,1])

            with col1:
                st.write(f"{name} (Qty: {data['qty']})")

            with col2:
                if st.button("➕", key=f"inc_{name}"):
                    st.session_state.cart[name]["qty"] += 1

            with col3:
                if st.button("➖", key=f"dec_{name}"):
                    if st.session_state.cart[name]["qty"] > 1:
                        st.session_state.cart[name]["qty"] -= 1
                    else:
                        del st.session_state.cart[name]

            subtotal += data["price"] * data["qty"]

        tax_rate = st.session_state.get("vat_rate", 12)
        tax = subtotal * (tax_rate / 100)

        total = round(subtotal + tax)  # Rounded

        st.divider()
        st.write(f"Subtotal: ${subtotal:.2f}")
        st.write(f"Tax ({tax_rate}%): ${tax:.2f}")
        st.write(f"**Total (Rounded): ${total}**")

        payment_method = st.radio("Payment", ["Cash", "Card", "Mobile Wallet"])

        if st.button("Complete Sale", use_container_width=True):
            if not st.session_state.cart:
                st.warning("Cart empty")
                return

            for name, data in st.session_state.cart.items():
                reduce_inventory(name, data["qty"])
                check_auto_reorder(name, data["qty"])

            post_sale(
                subtotal=subtotal,
                discount=0,
                tax=tax,
                total=total,
                payment_method=payment_method
            )

            st.session_state.cart = {}
            st.success("Sale Completed")
