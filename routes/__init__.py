# name:   __init__.py
# author: Jordan Stremming
#
# Provides routing for application to different route files.
#

from flask import Blueprint

# define each route file below here
routes = Blueprint('routes', __name__)
from . import index  # noqa: E402
from . import cart_processing  # noqa: E402
