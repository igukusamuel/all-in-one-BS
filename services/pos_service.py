from core.inventory import reduce_inventory
from core.accounting import post_sale

def process_sale(cart, total, payment_method):
    for product, qty in cart.items():
        reduce_inventory(product, qty)

    post_sale(total, payment_method)

