import streamlit as st
from core.inventory import get_inventory, reduce_inventory, check_auto_reorder
from core.accounting import post_sale

CRITICAL_THRESHOLD = 15
TAX_RATE_DEFAULT = 0.12  # 12% VAT default


def pos_screen():

    # -----------------------------
    # INIT SESSION STATE
    # -----------------------------
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "pos"

    # -----------------------------
    # ROUTING
    # -----------------------------
    if st.session_state.view_mode != "pos":
        from ui.close_shift_ui import close_shift_screen
        close_shift_screen()
        return

    st.title("Point of Sale")

    inventory = get_inventory()

    # -----------------------------
    # CATEGORY SELECTION
    # -----------------------------
    col_cat, col_products, col_cart = st.columns([1, 3, 1.5])

    with col_cat:
        st.subheader("Categories")
        categories = sorted(set(item["category"] for item in inventory))
        selected_category = st.radio(
            "Select Category",
            categories,
            label_visibility="collapsed"
        )

    # -----------------------------
    # PRODUCT GRID
    # -----------------------------
    with col_products:
        st.subheader(selected_category)
        filtered = [i for i in inventory if i["category"] == selected_category]

        cols_per_row = 3
        rows = (len(filtered) + cols_per_row - 1) // cols_per_row

        for r in range(rows):
            cols = st.columns(cols_per_row)
            for c in range(cols_per_row):
                idx = r * cols_per_row + c
                if idx < len(filtered):
                    item = filtered[idx]
                    available_stock = item["stock"] - st.session_state.cart.get(item["name"], {}).get("qty", 0)
                    stock_warning = ""
                    if available_stock <= CRITICAL_THRESHOLD:
                        stock_warning = f" ⚠ Low Stock ({available_stock})"

                    with cols[c]:
                        st.markdown(
                            f"""
                            <div style='border:1px solid #ddd; padding:10px; border-radius:5px;'>
                                <h4>{item['name']}</h4>
                                <p>Price: ${item['price']}</p>
                                <p>Stock: {available_stock}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button(f"Add {item['name']}", key=item['name']):
                            if item["name"] in st.session_state.cart:
                                st.session_state.cart[item["name"]]["qty"] += 1
                            else:
                                st.session_state.cart[item["name"]] = {
                                    "price": item["price"],
                                    "qty": 1
                                }

    # -----------------------------
    # CART PANEL
    # -----------------------------
    with col_cart:
        st.subheader("Cart")
        subtotal = 0

        # Show cart items
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

        # Discount
        discount_percent = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
        discount_amount = subtotal * (discount_percent / 100)
        taxable_amount = subtotal - discount_amount

        # VAT option
        vat_inclusive = st.checkbox("VAT Inclusive Price", value=False)
        vat_rate = st.number_input("VAT (%)", 0.0, 100.0, TAX_RATE_DEFAULT * 100)

        if vat_inclusive:
            subtotal_ex_vat = taxable_amount / (1 + vat_rate / 100)
            tax_amount = taxable_amount - subtotal_ex_vat
            total = taxable_amount
        else:
            tax_amount = taxable_amount * (vat_rate / 100)
            total = taxable_amount + tax_amount

        st.write(f"Discount: -${discount_amount:.2f}")
        st.write(f"Tax: +${tax_amount:.2f}")
        st.write(f"**Total: ${total:.2f}**")

        # -----------------------------
        # Payment Methods
        # -----------------------------
        payment_method = st.radio(
            "Payment Method",
            ["Cash", "Card", "Mobile Wallet"]
        )

        cash_received = 0
        change_due = 0
        if payment_method == "Cash":
            cash_received = st.number_input("Cash Received", min_value=0.0, step=1.0)
            change_due = cash_received - total
            if cash_received > 0:
                st.write(f"Change Due: ${change_due:.2f}")

        st.divider()

        # -----------------------------
        # Complete Sale Button
        # -----------------------------
        if st.button("Complete Sale", use_container_width=True):

            if total <= 0 or len(st.session_state.cart) == 0:
                st.warning("Cart is empty.")
                return

            if payment_method == "Cash" and cash_received < total:
                st.warning("Insufficient cash received.")
                return

            # Reduce inventory & check auto-reorder
            for name, data in st.session_state.cart.items():
                reduce_inventory(name, data["qty"])
                check_auto_reorder(name, data["qty"])  # triggers reorder if needed

            # Post to accounting engine
            post_sale(
                subtotal=subtotal,
                discount=discount_amount,
                tax=tax_amount,
                total=total,
                payment_method=payment_method
            )

            # Update shift cash
            if payment_method == "Cash":
                st.session_state.shift["cash_sales"] += total

            st.session_state.cart = {}
            st.success("Sale Completed")
            st.rerun()

        st.divider()

        # -----------------------------
        # Close Shift Button
        # -----------------------------
        if st.button("Close Shift", use_container_width=True):
            st.session_state.view_mode = "close_shift"
            st.rerun()

    # -----------------------------
    # Barcode Scanner Support
    # -----------------------------
    barcode_input = st.text_input("Scan Barcode")
    if barcode_input:
        product = next((i for i in inventory if i.get("barcode") == barcode_input), None)
        if product:
            if product["name"] in st.session_state.cart:
                st.session_state.cart[product["name"]]["qty"] += 1
            else:
                st.session_state.cart[product["name"]] = {"price": product["price"], "qty": 1}
            st.experimental_rerun()
