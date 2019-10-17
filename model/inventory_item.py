# name:   inventory_item.py
# author:
#
# description
#


class InventoryItem:
    def __init__(self, id_=None, name="", description="",
                 price=0.00, category=None):
        self.id_ = id_
        self.name = name
        self.description = description
        self.price = price
        self.category = category
