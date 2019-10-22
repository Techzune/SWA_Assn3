# name:   category.py
# author: Jordan Stremming
#
# Enumerator for inventory items
#
from enum import Enum


class ItemCategory(Enum):
    HOUSEHOLD_ITEMS = 'Household Items',
    BOOKS = 'Books',
    TOYS = 'Toys',
    SMALL_ELECTRONICS = 'Small Electronics'
