import streamlit as st


def post_sale(subtotal, discount, tax, total):

    if "ledger" not in st.session_state:
        st.session_state.ledger = []

    journal_entry = {
        "debits": [],
        "credits": []
    }

    # Debit Cash
    journal_entry["debits"].append({
        "account": "Cash",
        "amount": total
    })

    # Debit Discount (if any)
    if discount > 0:
        journal_entry["debits"].append({
            "account": "Discount Expense",
            "amount": discount
        })

    # Credit Revenue
    journal_entry["credits"].append({
        "account": "Revenue",
        "amount": subtotal
    })

    # Credit Tax
    if tax > 0:
        journal_entry["credits"].append({
            "account": "Tax Payable",
            "amount": tax
        })

    st.session_state.ledger.append(journal_entry)

    return journal_entry
