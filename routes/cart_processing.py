
from flask import render_template, request
from models import shopping_cart
from . import routes
from db import add_purchase
import json


@routes.route('/cart_build', methods=['POST'])
def cart_build():
    """
    Builds the cart based on data given from the client's localstorage cart

    Params needed: username, cart (json string of shopping_cart obj)
    :returns: shopping_cart, a built version of a user's cart
    """
    cart_json = json.loads(request.form['cart'])  # Might be bugged. Content were also stringified.
    cart_obj = shopping_cart.ShoppingCart(request.form['username'])
    for i in cart_json:  # Might need to unwrap before adding to object
        # obj = json.loads(i)
        # cart_obj.add_inventory_item(obj)
        cart_obj.add_inventory_item(i)
    return cart_obj


@routes.route('/purchase', methods=['POST'])
def purchase():
    """
    Builds the cart based on data given from the client's localstorage cart

    Params needed: username, cart (json string of shopping_cart obj)
    :returns: bool, true when db.add_purchase successfully called
    """
    cart = cart_build()
    user_purchase = cart.to_purchase(request.form['address'], request.form['credit_card'])
    add_purchase(user_purchase)
    return True
