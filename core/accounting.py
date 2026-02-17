import streamlit as st

def post_sale(total):
    if "gl" not in st.session_state:
        st.session_state.gl = []

    cost_total = total / 2  # assuming 50% cost

    # Revenue entry
    st.session_state.gl.append({
        "debit": "Cash",
        "credit": "Revenue",
        "amount": total
    })

    # COGS entry
    st.session_state.gl.append({
        "debit": "COGS",
        "credit": "Inventory",
        "amount": cost_total
    })

