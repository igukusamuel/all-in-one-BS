import json
from datetime import datetime

LEDGER_PATH = "data/ledger.json"

def load_ledger():
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_ledger(entries):
    with open(LEDGER_PATH, "w") as f:
        json.dump(entries, f, indent=4)

def post_sale(total, payment_method):
    ledger = load_ledger()

    entry = {
        "date": str(datetime.now()),
        "type": "SALE",
        "amount": total,
        "payment_method": payment_method
    }

    ledger.append(entry)
    save_ledger(ledger)
