import json
from core.config import LOW_STOCK_THRESHOLD

DATA_PATH = "data/products.json"

def get_inventory():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_inventory(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def reduce_inventory(product_name, qty):
    data = get_inventory()

    for item in data:
        if item["name"] == product_name:
            if item["stock"] < qty:
                raise ValueError("Insufficient stock")
            item["stock"] -= qty

    save_inventory(data)

def get_low_stock_items():
    return [p for p in get_inventory() if p["stock"] <= LOW_STOCK_THRESHOLD]
