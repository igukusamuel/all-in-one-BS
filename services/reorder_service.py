
from core.inventory import get_low_stock_items

def check_auto_reorder():
    return get_low_stock_items()
