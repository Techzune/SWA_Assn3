# name:   index.py
# author: Jordan Stremming
#
# Provides the index routing of the application
#
import flask
from flask import render_template, request, redirect
from flask_login import login_user, current_user, logout_user

import db
from models import User
from . import routes


@routes.route('/', methods=['GET', 'POST'])
def index():
    """Home page"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.get_user(User(username=username, password=password))
        if user is not None:
            login_user(user)
            flask.flash("Logged in successfully!", "success")
        else:
            flask.flash("Invalid username or password.", "error")

    return render_template('index.jinja2')


@routes.route('/logout')
def logout():
    logout_user()
    flask.flash("You are no longer logged in!", "success")
    return redirect('/')
