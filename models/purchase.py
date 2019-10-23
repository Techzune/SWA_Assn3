# name:   purchase.py
# author:
#
# description
#


class Purchase:
    def __init__(self, id_=None, username=None, items=None, total_price=0.00,
                 credit_card=None, address=None):
        """
        Creates a user's purchase for database storage.

        :param id_: int, optional, the id of the purchase
        :param username: str, user's username
        :param items: list, ShoppingCartItems associated with purchase
        :param total_price: float, total cost
        :param credit_card: str, credit card info
        :param address: Address, address
        """
        self.id_ = id_
        self.username = username
        self.items = items
        self.total_price = total_price
        self.credit_card = credit_card
        self.address = address
