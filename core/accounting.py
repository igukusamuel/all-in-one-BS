import streamlit as st

def post_sale(subtotal, discount, tax, total, payment_method):
    if "ledger" not in st.session_state:
        st.session_state.ledger = []
    st.session_state.ledger.append({
        "type": "sale",
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "payment_method": payment_method
    })

def get_ledger():
    if "ledger" not in st.session_state:
        st.session_state.ledger = []
    return st.session_state.ledger
