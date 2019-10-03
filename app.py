# name:   app.py
# author: Jordan Stremming
#
# Initializes the Flask application:
# * renders stylesheets (.scss to .css)
# * sets up database connection (w/ teardown)
# * launches development server
#

import sqlite3

from flask import Flask, g
from flask_assets import Environment, Bundle

from routes import *

# ===============================================
# Initialize Flask application
# ===============================================
app = Flask(__name__)
app.register_blueprint(routes)


# ===============================================
# Render stylesheets (.scss to .css)
# ===============================================
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('site.scss', filters='libsass', output='site.css')
assets.register('scss_all', scss)


# ===============================================
# Set up database connection and teardown
# (SOURCE: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/)
# ===============================================


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("./data.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ===============================================
# Launch the development server
# ===============================================
if __name__ == '__main__':
    app.run()
