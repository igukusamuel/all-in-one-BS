import streamlit as st
from core.accounting import load_ledger

def ledger_screen():
    st.title("Sales Ledger")
    ledger = load_ledger()
    st.json(ledger)

