import streamlit as st

# Initialize inventory in session_state for demo
def get_inventory():
    if "inventory" not in st.session_state:
        st.session_state.inventory = [
            # Beverages
            {"name": "Espresso", "category": "Beverages", "price": 3.0, "stock": 50, "min_stock": 10, "reorder_qty": 50, "supplier": "ABC Coffee", "image": "images/espresso.jpg", "barcode": "100001"},
            {"name": "Latte", "category": "Beverages", "price": 4.5, "stock": 30, "min_stock": 10, "reorder_qty": 40, "supplier": "ABC Coffee", "image": "images/latte.jpg", "barcode": "100002"},
            {"name": "Cappuccino", "category": "Beverages", "price": 4.0, "stock": 20, "min_stock": 5, "reorder_qty": 30, "supplier": "ABC Coffee", "image": "images/cappuccino.jpg", "barcode": "100003"},
            {"name": "Iced Coffee", "category": "Beverages", "price": 5.0, "stock": 10, "min_stock": 5, "reorder_qty": 20, "supplier": "ABC Coffee", "image": "images/iced_coffee.jpg", "barcode": "100004"},
            {"name": "Tea", "category": "Beverages", "price": 2.5, "stock": 100, "min_stock": 20, "reorder_qty": 50, "supplier": "Tea Co", "image": "images/tea.jpg", "barcode": "100005"},

            # Snacks
            {"name": "Croissant", "category": "Snacks", "price": 3.5, "stock": 15, "min_stock": 5, "reorder_qty": 20, "supplier": "Bakery Co", "image": "images/croissant.jpg", "barcode": "200001"},
            {"name": "Muffin", "category": "Snacks", "price": 3.0, "stock": 40, "min_stock": 10, "reorder_qty": 30, "supplier": "Bakery Co", "image": "images/muffin.jpg", "barcode": "200002"},
            {"name": "Bagel", "category": "Snacks", "price": 2.5, "stock": 60, "min_stock": 15, "reorder_qty": 40, "supplier": "Bakery Co", "image": "images/bagel.jpg", "barcode": "200003"},
            {"name": "Sandwich", "category": "Snacks", "price": 6.0, "stock": 12, "min_stock": 5, "reorder_qty": 15, "supplier": "Bakery Co", "image": "images/sandwich.jpg", "barcode": "200004"},
            {"name": "Cookie", "category": "Snacks", "price": 2.0, "stock": 200, "min_stock": 50, "reorder_qty": 100, "supplier": "Bakery Co", "image": "images/cookie.jpg", "barcode": "200005"},
        ]
    return st.session_state.inventory


def reduce_inventory(name, qty):
    for item in st.session_state.inventory:
        if item["name"] == name:
            item["stock"] -= qty
            if item["stock"] < 0:
                item["stock"] = 0
            break


def check_auto_reorder(product_name, sold_qty=0):
    """
    Deducts stock and triggers auto-reorder if stock <= min_stock.
    """
    for item in st.session_state.inventory:
        if item["name"] == product_name:
            # Deduct sold quantity
            item["stock"] -= sold_qty
            if item["stock"] < 0:
                item["stock"] = 0

            # Auto-reorder
            if item["stock"] <= item.get("min_stock", 10):
                # Here you could trigger API/email to supplier
                st.info(f"Auto-order triggered for {product_name} from {item['supplier']}, reorder qty={item['reorder_qty']}")
            break
