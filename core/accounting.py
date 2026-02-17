import streamlit as st

def post_sale(subtotal, discount, tax, total):
    """
    Posts a retail sale into the accounting engine.
    Assumes cash sale for now.
    """

    journal_entry = {
        "debits": [
            {"account": "Cash", "amount": total},
            {"account": "Discount Expense", "amount": discount} if discount > 0 else None,
        ],
        "credits": [
            {"account": "Revenue", "amount": subtotal},
            {"account": "Tax Payable", "amount": tax} if tax > 0 else None,
        ],
    }

    # Remove None entries
    journal_entry["debits"] = [d for d in journal_entry["debits"] if d]
    journal_entry["credits"] = [c for c in journal_entry["credits"] if c]

    # For now just print — later store in DB
    print("Journal Entry Posted:")
    print(journal_entry)

    return journal_entry
