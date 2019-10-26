# name:   shopping_cart.py
# author: Jordan Stremming
#
# Model for user's shopping cart
#
from models import ShoppingCartItem, Purchase


class ShoppingCart:
    def __init__(self, user=None, items_dict=None):
        """
        Creates a user's shopping cart.

        :param user: User, the associate user of the owner.
        :param items_dict: optional, dictionary {item_id, ShoppingCartItem}
        """
        self.user = user
        self.items_dict = items_dict or {}

    def add_inventory_item(self, inv_item, qty=1):
        """
        Adds a qty of InventoryItem to ShoppingCart.
        If the item is already in the cart, the qty will be updated.

        :param inv_item: InventoryItem, the item to add to.
        :param qty: int, the quantity to add. Defaults to 1.
        """
        if inv_item.id_ in self.items_dict.keys():
            self.items_dict[inv_item.id_].qty += qty
        else:
            item = ShoppingCartItem
            item.item = inv_item
            item.price = inv_item.price
            item.qty = qty
            self.items_dict[inv_item.id_] = item

    def remove_inventory_item(self, inv_item, qty=-1):
        """
        Removes a qty of InventoryItem from the ShoppingCart.
        If qty is -1, remove item entirely.

        :param inv_item: InventoryItem, item to remove from.
        :param qty: int, the quantity to remove. Defaults to -1.
        """
        if qty == -1:
            self.items_dict.pop(inv_item.id_)
        else:
            if inv_item.id_ in self.items_dict.keys():
                self.items_dict[inv_item.id_].qty -= qty

    def list_all(self):
        """
        Generates a list of ShoppingCartItems
        :return: list, all ShoppingCartItems in ShoppingCart
        """
        return list(self.items_dict.values())

    def total_price(self):
        """
        Calculates the total price of ShoppingCart
        :return: float, the total price
        """
        items = self.list_all()
        price = 0.00
        for item in items:
            price += item.price * item.qty
        return price

    def to_purchase(self, address, credit_card_num):
        """
        Converts ShoppingCart to Purchase.

        :param address: Address, address for purchase
        :param credit_card_num: String, credit card number
        :return: Purchase, associated with order
        """
        return Purchase(username=self.user.username, items=self.list_all(),
                        address=address, credit_card=credit_card_num,
                        total_price=self.total_price())
