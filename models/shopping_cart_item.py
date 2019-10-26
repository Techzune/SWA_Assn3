# name:   shopping_cart_item.py
# author: Jordan Stremming
#
# Model for item in shopping cart
#
import locale

locale.setlocale(locale.LC_ALL, '')


class ShoppingCartItem:
    def __init__(self, item=None, qty=0, price=0.00):
        """
        Creates an item for a shopping cart.

        :param item: InventoryItem, the item
        :param qty: int, the quantity
        :param price: float, the price of the item
        """
        self.item = item
        self.qty = qty
        self.price = price

    @property
    def price_as_str(self):
        return locale.currency(self.price)
