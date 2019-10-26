# name:   shopping_cart.py
# author: Jordan Stremming
#
# Model for user's shopping cart
#
from models import Purchase, locale

locale.setlocale(locale.LC_ALL, '')


class ShoppingCart:
    def __init__(self, user=None, items=None):
        """
        Creates a user's shopping cart.

        :param user: User, the associate user of the owner.
        :param items: optional, list of ShoppingCartItem
        """
        self.user = user
        self.items = items or []

    @property
    def total_price(self):
        """
        Calculates the total price of ShoppingCart
        :return: float, the total price
        """
        price = 0.00
        for item in self.items:
            price += (item.price or 0) * (item.qty or 1)
        return price

    @property
    def total_price_as_str(self):
        return locale.currency(self.total_price)

    def to_purchase(self, address, credit_card_num):
        """
        Converts ShoppingCart to Purchase.

        :param address: Address, address for purchase
        :param credit_card_num: String, credit card number
        :return: Purchase, associated with order
        """
        return Purchase(username=self.user.username, items=self.items,
                        address=address, credit_card=credit_card_num,
                        total_price=self.total_price)
