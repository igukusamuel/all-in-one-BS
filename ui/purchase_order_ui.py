import streamlit as st

def purchase_order_screen():
    st.subheader("Purchase Orders (Auto / Manual)")
    pending_po = st.session_state.get("pending_po", [])

    if not pending_po:
        st.info("No pending orders.")
        return

    for idx, po in enumerate(pending_po):
        st.write(f"{idx+1}. {po['product']} → Qty: {po['qty']}")
        if st.button(f"Submit PO {po['product']}", key=f"po_{po['product']}"):
            st.success(f"PO for {po['product']} submitted")
            pending_po.pop(idx)
            st.session_state.pending_po = pending_po
            break
