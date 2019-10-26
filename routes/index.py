# name:   index.py
# author: Jordan Stremming
#
# Provides the index routing of the application
#
import flask
from flask import render_template, request, redirect
from flask_login import login_user, current_user, logout_user, login_required

import db
from models import User, InventoryItem, ShoppingCartItem
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

    return redirect('/inventory')


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flask.flash("You are no longer logged in!", "success")
    return redirect('/')


@routes.route('/cart')
@login_required
def cart():
    return render_template('cart.jinja2', cart=db.get_shopping_cart(user=User(id_=current_user.get_id())))


@routes.route('/cart/add', methods=['GET'])
def cart_add():
    if request.args.get('id') is None:
        return redirect('/inventory')

    db.add_to_cart(user=User(current_user.get_id()),
                   item=db.get_inventory_item(InventoryItem(id_=request.args.get('id'))))
    return redirect('/cart')


@routes.route('/cart/remove', methods=['GET'])
def cart_remove():
    if request.args.get('id') is None:
        return redirect('/cart')

    id_ = request.args.get('id')
    qty = request.args.get('qty')

    db.remove_from_cart(user=User(current_user.get_id()),
                        item=ShoppingCartItem(item=InventoryItem(id_=id_), qty=qty))
    return redirect('/cart')


@routes.route('/history')
@login_required
def history():
    return render_template('history.jinja2')


@routes.route('/inventory')
def inventory():
    return render_template('inventory.jinja2', inventory=db.get_inventory())
