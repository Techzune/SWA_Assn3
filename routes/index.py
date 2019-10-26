# name:   index.py
# author: Jordan Stremming
#
# Provides the index routing of the application
#
import flask
from flask import render_template, request, redirect
from flask_login import login_user, current_user, logout_user, login_required

import db
from models import User, InventoryItem, ShoppingCartItem, Purchase, Address
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
                        item=ShoppingCartItem(item=InventoryItem(id_=id_)), qty=qty)
    return redirect('/cart')


@routes.route('/cart/update', methods=['GET'])
def cart_update():
    for id_, qty in request.args.items():
        # this makes sure we only use ints
        # noinspection PyBroadException
        try:
            qty = int(qty)
            db.update_cart(user=User(current_user.get_id()), item=ShoppingCartItem(item=InventoryItem(id_=id_)),
                           qty=qty)
        except Exception:
            continue
    return redirect('/cart')


@routes.route('/cart/purchase', methods=['POST'])
def cart_purchase():
    credit_card = request.form.get("card")
    street = request.form.get("address")
    street2 = request.form.get("address2")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip")

    user = db.get_user(User(current_user.get_id()))
    user_cart = db.get_shopping_cart(user)

    if len(user_cart.items) == 0:
        flask.flash("You don't have anything to purchase!", "info")

    elif '' not in [credit_card, street, city, state, zip_code]:
        address = Address(street=street, street2=street2, city=city, state=state, zip_code=zip_code)

        purchase = Purchase(username=user.username, items=user_cart.items,
                            total_price=user_cart.total_price, address=address,
                            credit_card=credit_card)

        db.add_purchase(purchase)
        db.clear_shopping_cart(user)
        flask.flash("Purchase complete!", "success")

    else:
        flask.flash("Invalid purchase! Did you fill all fields?", "error")

    return redirect("/cart")


@routes.route('/history')
@login_required
def history():
    user = db.get_user(User(current_user.get_id()))
    return render_template('history.jinja2', purchases=db.get_user_purchases(user))


@routes.route('/inventory')
def inventory():
    return render_template('inventory.jinja2', inventory=db.get_inventory())
