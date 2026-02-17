def open_shift(float_amount):
    return {
        "is_open": True,
        "beginning_cash": float_amount,
        "cash_sales": 0
    }

def close_shift(shift_data, actual_cash):
    expected = shift_data["beginning_cash"] + shift_data["cash_sales"]
    variance = actual_cash - expected
    return expected, variance

