import streamlit as st
from ui.purchase_order_ui import purchase_order_screen
from core.accounting import get_ledger
from core.staff import get_staff, add_staff_member

def admin_dashboard():
    st.title("Admin Dashboard")

    menu = st.sidebar.radio("Navigation", [
        "Dashboard Home",
        "PO & Sales Ledger",
        "Ordering / Auto-Reorder",
        "Staff Management",
        "Store Settings"
    ])

    if menu == "Dashboard Home":
        st.subheader("Overview")
        st.info("Summary of sales, inventory, and orders will appear here.")
        # Optionally add KPIs, charts, totals

    elif menu == "PO & Sales Ledger":
        st.subheader("Purchase Orders & Sales Ledger")
        ledger = get_ledger()  # returns all POs + sales
        for idx, entry in enumerate(ledger):
            st.markdown(f"### Entry {idx+1}")
            st.write("Debits:", entry.get("debits", []))
            st.write("Credits:", entry.get("credits", []))
            st.divider()

    elif menu == "Ordering / Auto-Reorder":
        st.subheader("Create / Approve Purchase Orders")
        purchase_order_screen()

    elif menu == "Staff Management":
        st.subheader("Staff Onboarding & Roles")
        staff_list = get_staff()
        st.write(staff_list)

        with st.form("add_staff"):
            name = st.text_input("Staff Name")
            role = st.selectbox("Role", ["Cashier", "Store Manager", "Driver"])
            submit = st.form_submit_button("Add Staff")
            if submit and name:
                add_staff_member(name, role)
                st.success(f"Added {name} as {role}")
                st.experimental_rerun()

    elif menu == "Store Settings":
        st.subheader("Configure Store Settings")
        # Example: VAT, minimum stock, payment options
        vat = st.number_input("VAT %", 0.0, 100.0, 12.0)
        min_stock = st.number_input("Default Minimum Stock", 0, 100, 10)
        st.write(f"VAT set to {vat}% and default minimum stock set to {min_stock}")
