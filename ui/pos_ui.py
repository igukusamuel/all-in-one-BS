import streamlit as st
from core.inventory import get_inventory, reduce_inventory
from core.accounting import post_sale

CRITICAL_THRESHOLD = 15
TAX_RATE_DEFAULT = 0.1


def pos_screen():

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    inventory = get_inventory()

    st.title("Point of Sale")

    col_cat, col_products, col_cart = st.columns([1, 2, 1.5])

    # -------------------------
    # CATEGORY PANE
    # -------------------------
    with col_cat:
        st.subheader("Categories")

        categories = sorted(set(item["category"] for item in inventory))

        selected_category = st.radio(
            "Select Category",
            categories,
            label_visibility="collapsed"
        )

    # -------------------------
    # PRODUCT GRID
    # -------------------------
    with col_products:
        st.subheader(selected_category)

        filtered = [i for i in inventory if i["category"] == selected_category]

        for item in filtered:
            stock_warning = ""
            if item["stock"] <= CRITICAL_THRESHOLD:
                stock_warning = f" ⚠ Low Stock ({item['stock']})"

            if st.button(
                f"{item['name']} - ${item['price']}{stock_warning}",
                use_container_width=True
            ):
                if item["name"] in st.session_state.cart:
                    st.session_state.cart[item["name"]]["qty"] += 1
                else:
                    st.session_state.cart[item["name"]] = {
                        "price": item["price"],
                        "qty": 1
                    }

    # -------------------------
    # CART PANEL
    # -------------------------
    with col_cart:
        st.subheader("Cart")

        subtotal = 0

        for name, data in list(st.session_state.cart.items()):

            col_a, col_b, col_c = st.columns([2, 1, 1])

            with col_a:
                st.write(name)

            with col_b:
                qty = st.number_input(
                    "Qty",
                    min_value=1,
                    value=data["qty"],
                    key=f"qty_{name}"
                )
                st.session_state.cart[name]["qty"] = qty

            with col_c:
                if st.button("❌", key=f"remove_{name}"):
                    del st.session_state.cart[name]
                    st.rerun()

            subtotal += data["price"] * data["qty"]

        st.divider()

        st.write(f"Subtotal: ${subtotal:.2f}")

        discount_percent = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
        discount_amount = subtotal * (discount_percent / 100)

        taxable_amount = subtotal - discount_amount

        tax_rate = st.number_input("Tax (%)", 0.0, 100.0, TAX_RATE_DEFAULT * 100)
        tax_amount = taxable_amount * (tax_rate / 100)

        total = taxable_amount + tax_amount

        st.write(f"Discount: -${discount_amount:.2f}")
        st.write(f"Tax: +${tax_amount:.2f}")
        st.write(f"**Total: ${total:.2f}**")

        st.divider()

        cash_received = st.number_input("Cash Received", min_value=0.0, step=1.0)

        change_due = cash_received - total

        if cash_received > 0:
            st.write(f"Change Due: ${change_due:.2f}")

        st.divider()

        # -------------------------
        # PAYMENT
        # -------------------------
        if st.button("Complete Sale", use_container_width=True):

            if total <= 0:
                st.warning("Cart is empty.")
                return

            if cash_received < total:
                st.warning("Insufficient cash received.")
                return

            # Reduce inventory
            for name, data in st.session_state.cart.items():
                reduce_inventory(name, data["qty"])

            # Post to accounting engine
            post_sale(
                subtotal=subtotal,
                discount=discount_amount,
                tax=tax_amount,
                total=total
            )

            st.session_state.shift["cash_sales"] += total
            st.session_state.cart = {}

            st.success("Sale Completed")
            st.rerun()
