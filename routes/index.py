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


@routes.route('/')
def index():
    """Home page"""
    return render_template('index.jinja2')


@routes.route('/logout')
def logout():
    logout_user()
    return redirect('/')
