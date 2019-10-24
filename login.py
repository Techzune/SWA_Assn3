import flask
from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from app import app
from db import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    userName = request.form.get('username')
    password = request.form.get('password')
    user = get_user(username='userName', password='password')
    if not user or not check_password_hash(user.password, password):
        flash('Username/password incorrect')
        return redirect(url_for('#login'))
    return redirect(url_for('http://127.0.0.1:5000/#home'))
