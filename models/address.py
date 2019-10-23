# name:   address.py
# author: Jordan Stremming
#
# Model for address associated with purchase
#


class Address:
    def __init__(self, street="", street2="", city="", state="", zip_code=""):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip_code = zip_code
