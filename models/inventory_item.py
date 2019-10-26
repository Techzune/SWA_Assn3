# name:   inventory_item.py
# author: Jordan Stremming
#
# Model for item in inventory
#


class InventoryItem():
    def __init__(self, id_=None, name="", description="",
                 price=0.00, category=None, qty=0):
        """
        Creates an item for the inventory.

        :param id_: int, optional, id of item
        :param name: str, name of item
        :param description: str, description of item
        :param price: float, cost of item
        :param category: ItemCategory, enumerator
        :param qty: int, quantity of item
        """
        self.id_ = id_
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.quantity = qty
