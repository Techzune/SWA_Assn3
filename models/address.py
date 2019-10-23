# name:   address.py
# author: Jordan Stremming
#
# Model for address associated with purchase
#


class Address:
    def __init__(self, street="", street2="", city="", state="", zip_code=""):
        """
        Creates an address for a purchase.

        :param street: str, street address
        :param street2: str, street address line 2
        :param city: str, city
        :param state: str, state
        :param zip_code: str, zip code
        """
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def to_str(self):
        return self.street + "||" + self.street2 + "||" + self.city + \
               "||" + self.state + "||" + self.zip_code

    def from_str(self, s):
        split = s.split("||")
        self.street = split[0]
        self.street2 = split[1]
        self.city = split[2]
        self.state = split[3]
        self.zip_code = split[4]
        return self
