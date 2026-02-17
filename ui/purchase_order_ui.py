import streamlit as st
from core.inventory import get_inventory, reduce_inventory
from core.accounting import post_purchase_order

def purchase_order_screen():
    st.title("Purchase Orders / Supplier Auto-Order")

    inventory = get_inventory()
    
    st.subheader("Items Below Minimum Stock")
    low_stock_items = [i for i in inventory if i["stock"] <= i.get("min_stock", 10)]
    
    po_items = {}
    
    if not low_stock_items:
        st.info("All stock levels are sufficient.")
    else:
        for item in low_stock_items:
            st.markdown(f"**{item['name']}** (Stock: {item['stock']}, Min: {item['min_stock']})")
            qty_to_order = st.number_input(
                f"Order Qty for {item['name']}",
                min_value=0,
                value=item.get("reorder_qty", 0),
                key=f"po_{item['name']}"
            )
            po_items[item["name"]] = {
                "supplier": item["supplier"],
                "qty": qty_to_order,
                "unit_price": item["price"]
            }

    st.divider()
    st.subheader("Manual Purchase Order (Optional)")
    for item in inventory:
        if item["name"] not in po_items:
            qty_manual = st.number_input(
                f"Manual Order Qty for {item['name']}",
                min_value=0,
                value=0,
                key=f"manual_{item['name']}"
            )
            if qty_manual > 0:
                po_items[item["name"]] = {
                    "supplier": item["supplier"],
                    "qty": qty_manual,
                    "unit_price": item["price"]
                }

    st.divider()
    total_po_value = sum(v["qty"] * v["unit_price"] for v in po_items.values())
    st.write(f"Total Purchase Order Value: ${total_po_value:.2f}")

    if st.button("Submit Purchase Order"):
        if not po_items:
            st.warning("No items selected for purchase.")
            return
        
        # Update inventory
        for name, data in po_items.items():
            for item in inventory:
                if item["name"] == name:
                    item["stock"] += data["qty"]
                    break
        
        # Post to accounting (Inventory debit, Accounts Payable credit)
        post_purchase_order(po_items)
        
        st.success("Purchase Order submitted successfully! Inventory updated.")
        st.experimental_rerun()
