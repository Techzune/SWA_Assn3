# name:   inventory.py
# author:
#
# description
#


class Inventory:
    def __init__(self, items=None):
        self.items = items or {}

    def add_item(self, inventory_item, quantity):
        self.items[inventory_item] = quantity

    def remove_item(self, inventory_item):
        self.items[inventory_item] = None
