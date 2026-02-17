import streamlit as st

def post_sale(subtotal, discount, tax, total, payment_method="Cash"):
    """
    Posts a retail sale to the ledger.
    Handles multiple payment methods: Cash, Card, Mobile Wallet
    """
    if "ledger" not in st.session_state:
        st.session_state.ledger = []

    journal_entry = {
        "debits": [],
        "credits": []
    }

    # Debit depending on payment method
    if payment_method == "Cash":
        journal_entry["debits"].append({"account": "Cash", "amount": total})
    elif payment_method == "Card":
        journal_entry["debits"].append({"account": "Card Payments Receivable", "amount": total})
    elif payment_method == "Mobile Wallet":
        journal_entry["debits"].append({"account": "Mobile Wallet Receivable", "amount": total})
    else:
        journal_entry["debits"].append({"account": "Other Receivable", "amount": total})

    # Discount as Expense
    if discount > 0:
        journal_entry["debits"].append({"account": "Discount Expense", "amount": discount})

    # Credit Revenue
    journal_entry["credits"].append({"account": "Revenue", "amount": subtotal})

    # Credit Tax
    if tax > 0:
        journal_entry["credits"].append({"account": "Tax Payable", "amount": tax})

    # Append to ledger
    st.session_state.ledger.append(journal_entry)

    # Debug: print for now
    print(f"Sale posted: Total=${total}, Method={payment_method}")
    return journal_entry

def post_purchase_order(po_items):
    """
    Posts a purchase order to the ledger.
    Debit Inventory, Credit Accounts Payable per supplier.
    """
    if "ledger" not in st.session_state:
        st.session_state.ledger = []

    journal_entry = {"debits": [], "credits": []}
    supplier_totals = {}

    # Aggregate total per supplier
    for name, data in po_items.items():
        supplier = data["supplier"]
        line_total = data["qty"] * data["unit_price"]
        supplier_totals[supplier] = supplier_totals.get(supplier, 0) + line_total

        # Inventory debit per item
        journal_entry["debits"].append({"account": f"Inventory - {name}", "amount": line_total})

    # Credit Accounts Payable per supplier
    for supplier, total in supplier_totals.items():
        journal_entry["credits"].append({"account": f"Accounts Payable - {supplier}", "amount": total})

    st.session_state.ledger.append(journal_entry)
    print("Purchase Order posted to ledger:", journal_entry)
    return journal_entry


def get_ledger():
    if "ledger" not in st.session_state:
        st.session_state.ledger = []
    return st.session_state.ledger

