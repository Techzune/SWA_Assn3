# name:   app.py
# author: Jordan Stremming
#
# Initializes the Flask application:
# * renders stylesheets (.scss to .css)
# * sets up database connection (w/ teardown)
# * launches development server
#

from flask import Flask
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
from db import *  # noqa: E402

# set force to True if you want database to be recreated on launch
create_db(force=False)

# ===============================================
# Launch the development server
# ===============================================
if __name__ == '__main__':
    app.run()
