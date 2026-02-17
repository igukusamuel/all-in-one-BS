import streamlit as st

def get_inventory():
    if "inventory" not in st.session_state:
        st.session_state.inventory = [
            {"name": "Coffee", "price": 10, "cost": 5, "stock": 1000}
        ]
    return st.session_state.inventory

def reduce_inventory(name, qty):
    for item in st.session_state.inventory:
        if item["name"] == name:
            item["stock"] -= qty

