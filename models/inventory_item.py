# name:   inventory_item.py
# author: Jordan Stremming
#
# Model for item in inventory
#


class InventoryItem:
    def __init__(self, id_=None, name="", description="",
                 price=0.00, category=None, qty=0):
        self.id_ = id_
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.quantity = qty
