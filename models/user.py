# name:   user.py
# author: Jordan Stremming
#
# Model for User account
#


class User:
    def __init__(self, id_=None, username=None, password=None):
        """
        Creates a model for a user.

        :param id_: int, optional, the user's ID
        :param username: str, the user's username
        :param password: str, the user's password
        """
        self.id_ = id_
        self.username = username
        self.password = password
