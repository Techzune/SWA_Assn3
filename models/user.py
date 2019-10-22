# name:   user.py
# author: Jordan Stremming
#
# Model for User account
#


class User:
    def __init__(self, id_=None, username=None, password=None):
        self.id_ = id_
        self.username = username
        self.password = password
