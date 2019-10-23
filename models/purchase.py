# name:   purchase.py
# author:
#
# description
#


class Purchase:
    def __init__(self, id_=None, username=None, items=None, total_price=0,
                 credit_card=None, address=None):
        self.id_ = id_
        self.username = username
        self.items = items
        self.total_price = total_price
        self.credit_card = credit_card
        self.address = address
