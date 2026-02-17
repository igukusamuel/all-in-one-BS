def open_shift(amount):
    return {
        "is_open": True,
        "beginning_cash": amount,
        "cash_sales": 0
    }

def record_cash_sale(shift, amount):
    shift["cash_sales"] += amount

def close_shift(shift, actual_cash):
    expected = shift["beginning_cash"] + shift["cash_sales"]
    variance = actual_cash - expected
    shift["is_open"] = False
    return expected, variance
