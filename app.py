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
from flask_login import LoginManager

from routes import *

# ===============================================
# Initialize Flask application
# ===============================================
from routes.index import unauthorized

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
# Flask-Login configuration
# ===============================================
app.secret_key = "SUPER SECRET YO!"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    id_ = int(user_id)
    return get_user(User(id_=id_))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return unauthorized()


# ===============================================
# Launch the development server
# ===============================================
if __name__ == '__main__':
    app.run()
