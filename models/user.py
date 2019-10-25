# name:   user.py
# author: Jordan Stremming
#
# Model for User account
#
from flask_login._compat import unicode


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
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return unicode(self.id_)


