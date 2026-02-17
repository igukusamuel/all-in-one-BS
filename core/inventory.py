import streamlit as st
import json

def load_products():
    try:
        with open("data/products.json") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open("data/products.json", "w") as f:
        json.dump(products, f, indent=2)

def get_inventory():
    if "inventory" not in st.session_state:
        st.session_state.inventory = load_products()
    return st.session_state.inventory

def reduce_inventory(name, qty):
    inventory = get_inventory()
    for item in inventory:
        if item["name"] == name:
            item["stock"] -= qty
    st.session_state.inventory = inventory
    save_products(inventory)

def check_auto_reorder(name, qty_sold):
    # Simple auto-reorder: if stock <= min_stock, create PO
    inventory = get_inventory()
    for item in inventory:
        if item["name"] == name and item["stock"] <= item.get("min_stock", 10):
            if "pending_po" not in st.session_state:
                st.session_state.pending_po = []
            st.session_state.pending_po.append({
                "product": name,
                "qty": item.get("reorder_qty", 50)
            })
