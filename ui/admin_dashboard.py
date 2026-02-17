import streamlit as st
from core.inventory import get_inventory
from core.accounting import get_ledger
from core.staff import get_staff, add_staff_member

def admin_dashboard():

    st.title("Admin Dashboard")

    menu = st.sidebar.radio("Admin Menu", [
        "Ordering",
        "Sales Ledger",
        "Staff Management",
        "Store Settings"
    ])

    inventory = get_inventory()

    # -------------------------
    # ORDERING GRID (4x4)
    # -------------------------
    if menu == "Ordering":

        categories = sorted(set(i["category"] for i in inventory))
        selected_category = st.sidebar.radio("Category", categories)

        filtered = [i for i in inventory if i["category"] == selected_category]

        if "order_cart" not in st.session_state:
            st.session_state.order_cart = {}

        cols_per_row = 4
        rows = (len(filtered) + cols_per_row - 1) // cols_per_row

        for r in range(rows):
            cols = st.columns(cols_per_row)
            for c in range(cols_per_row):
                idx = r * cols_per_row + c
                if idx < len(filtered):
                    item = filtered[idx]
                    with cols[c]:
                        st.markdown(f"### {item['name']}")
                        st.write(f"Stock: {item['stock']}")

                        qty = st.session_state.order_cart.get(item["name"], 0)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("➕", key=f"order_inc_{item['name']}"):
                                st.session_state.order_cart[item["name"]] = qty + 1
                        with col2:
                            if st.button("➖", key=f"order_dec_{item['name']}"):
                                if qty > 0:
                                    st.session_state.order_cart[item["name"]] = qty - 1

                        st.write(f"Order Qty: {st.session_state.order_cart.get(item['name'],0)}")

                        if st.button("Place Order", key=f"place_{item['name']}"):
                            st.success(f"PO placed for {item['name']} ({st.session_state.order_cart.get(item['name'],0)} units)")
                            st.session_state.order_cart[item["name"]] = 0

    # -------------------------
    # SALES LEDGER
    # -------------------------
    elif menu == "Sales Ledger":
        ledger = get_ledger()
        if not ledger:
            st.info("No sales yet")
        for entry in ledger:
            st.write(entry)
            st.divider()

    # -------------------------
    # STAFF MANAGEMENT
    # -------------------------
    elif menu == "Staff Management":
        staff = get_staff()
        for s in staff:
            st.write(f"{s['name']} → {s['role']}")

        with st.form("add_staff"):
            name = st.text_input("Name")
            role = st.selectbox("Role", ["cashier", "admin"])
            if st.form_submit_button("Add"):
                add_staff_member(name, role)
                st.success("Staff added")
                st.rerun()

    # -------------------------
    # STORE SETTINGS
    # -------------------------
    elif menu == "Store Settings":
        vat = st.number_input("VAT %", 0.0, 100.0, 12.0)
        st.session_state.vat_rate = vat
        st.success("VAT Updated")
