# name:   index.py
# author: Jordan Stremming
#
# Provides the index routing of the application
#

from flask import render_template
from . import routes


@routes.route('/')
def index():
    """Home page"""
    return render_template('index.jinja2')
