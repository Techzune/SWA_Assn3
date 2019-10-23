# name:   shopping_cart_item.py
# author: Jordan Stremming
#
# Model for item in shopping cart
#


class ShoppingCartItem:
    def __init__(self, item_id=None, qty=0, price=0.00):
        """
        Creates an item for a shopping cart.

        :param item_id: int, the InventoryItem id
        :param qty: int, the quantity
        :param price: float, the price of the item
        """
        self.item_id = item_id
        self.qty = qty
        self.price = price
