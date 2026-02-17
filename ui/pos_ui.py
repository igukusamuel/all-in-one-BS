import streamlit as st
from PIL import Image
from core.inventory import get_inventory, reduce_inventory, check_auto_reorder
from core.accounting import post_sale
from ui.purchase_order_ui import purchase_order_screen

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
    if "auto_po_triggered" not in st.session_state:
        st.session_state.auto_po_triggered = False

    inventory = get_inventory()

    # -----------------------------
    # Auto-Reorder Trigger
    # -----------------------------
    low_stock_items = [i for i in inventory if i["stock"] <= i.get("min_stock", 10)]
    if low_stock_items and not st.session_state.auto_po_triggered:
        st.session_state.view_mode = "purchase_order"
        st.session_state.auto_po_triggered = True
        st.experimental_rerun()

    # -----------------------------
    # Show PO screen if triggered
    # -----------------------------
    if st.session_state.view_mode == "purchase_order":
        purchase_order_screen()
        return

    # -----------------------------
    # POS UI
    # -----------------------------
    st.title("Point of Sale")

    col_cat, col_products, col_cart = st.columns([1, 3, 1.5])

    # -----------------------------
    # CATEGORY SELECTION
    # -----------------------------
    with col_cat:
        st.subheader("Categories")
        categories = sorted(set(item["category"] for item in inventory))
        selected_category = st.radio("Select Category", categories, label_visibility="collapsed")

    # -----------------------------
    # PRODUCT GRID (3x4) with images
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
                        if item.get("image"):
                            try:
                                img = Image.open(item["image"])
                                st.image(img, width=100)
                            except:
                                st.write("No image")
                        st.markdown(
                            f"<div style='border:1px solid #ddd; padding:5px; border-radius:5px;'>"
                            f"<h4>{item['name']}</h4>"
                            f"<p>Price: ${item['price']}</p>"
                            f"<p>Stock: {available_stock}</p>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        # Add to cart
                        if st.button(f"Add {item['name']}", key=item['name']):
                            if item["name"] in st.session_state.cart:
                                st.session_state.cart[item["name"]]["qty"] += 1
                            else:
                                st.session_state.cart[item["name"]] = {"price": item["price"], "qty": 1}

    # -----------------------------
    # CART PANEL with + / - buttons
    # -----------------------------
    with col_cart:
        st.subheader("Cart")
        subtotal = 0

        for name, data in list(st.session_state.cart.items()):
            st.write(name)
            col_qty, col_inc, col_dec, col_remove = st.columns([2, 1, 1, 1])
            with col_qty:
                st.write(f"Qty: {data['qty']}")
            with col_inc:
                if st.button("+", key=f"inc_{name}"):
                    st.session_state.cart[name]["qty"] += 1
                    st.experimental_rerun()
            with col_dec:
                if st.button("-", key=f"dec_{name}"):
                    st.session_state.cart[name]["qty"] -= 1
                    if st.session_state.cart[name]["qty"] <= 0:
                        del st.session_state.cart[name]
                    st.experimental_rerun()
            with col_remove:
                if st.button("❌", key=f"rm_{name}"):
                    del st.session_state.cart[name]
                    st.experimental_rerun()

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

        # Payment Methods
        payment_method = st.radio("Payment Method", ["Cash", "Card", "Mobile Wallet"])
        cash_received = 0
        change_due = 0
        if payment_method == "Cash":
            cash_received = st.number_input("Cash Received", min_value=0.0, step=1.0)
            change_due = cash_received - total
            if cash_received > 0:
                st.write(f"Change Due: ${change_due:.2f}")

        st.divider()

        # Complete Sale
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
                check_auto_reorder(name, data["qty"])

            post_sale(
                subtotal=subtotal,
                discount=discount_amount,
                tax=tax_amount,
                total=total,
                payment_method=payment_method
            )

            st.session_state.cart = {}
            st.success("Sale Completed")
            st.experimental_rerun()

        st.divider()
        if st.button("Close Shift", use_container_width=True):
            st.session_state.view_mode = "close_shift"
            st.experimental_rerun()

    # -----------------------------
    # Barcode Scanner
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
