def get_inventory():
    return [
        # BEVERAGES
        {"name": "Espresso", "category": "Beverages", "price": 3.0, "stock": 50},
        {"name": "Latte", "category": "Beverages", "price": 4.5, "stock": 30},
        {"name": "Cappuccino", "category": "Beverages", "price": 4.0, "stock": 20},
        {"name": "Iced Coffee", "category": "Beverages", "price": 5.0, "stock": 10},
        {"name": "Tea", "category": "Beverages", "price": 2.5, "stock": 100},

        # SNACKS
        {"name": "Croissant", "category": "Snacks", "price": 3.5, "stock": 15},
        {"name": "Muffin", "category": "Snacks", "price": 3.0, "stock": 40},
        {"name": "Bagel", "category": "Snacks", "price": 2.5, "stock": 60},
        {"name": "Sandwich", "category": "Snacks", "price": 6.0, "stock": 12},
        {"name": "Cookie", "category": "Snacks", "price": 2.0, "stock": 200},
    ]


def reduce_inventory(name, quantity):
    # Replace with DB logic later
    pass

def check_auto_reorder(product_name, sold_qty):
    """
    Checks if stock is below minimum threshold and triggers reorder.
    For MVP, just print a message.
    """
    inventory = get_inventory()
    product = next((i for i in inventory if i["name"] == product_name), None)
    if not product:
        return
    product["stock"] -= sold_qty
    if product["stock"] <= product.get("min_stock", 10):
        print(f"Auto-reorder triggered for {product_name}, stock={product['stock']}")
