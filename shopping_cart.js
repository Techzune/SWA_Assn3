/*
* name: shopping_cart.js
* author: Steven Huynh
*
* Save shopping cart to localstorage for persistent cart
*
*/

<script
  src="https://code.jquery.com/jquery-3.4.1.min.js"
  integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
  crossorigin="anonymous"/>
// this will likely be written using AJAX

// Check for pre-existing cart data in localstorage
// yes: load it into shopping_cart object
// no: load empty shopping_cart object

// functions that will transfer button presses into their .py

// add one more of an item
// if the item doesn't exist in cart, then create it
function add_item(item_id, item_stringify){
  var test_item = localStorage.getItem(item_id);
  var item;
  if (test_item != null) {
    item = JSON.parse(test_item);
    item.qty++;
    test_item = JSON.stringify(item);
    localStorage.setItem(item_id, test_item)
  } else {
    item = JSON.parse(item_stringify);
    item.qty = 1;
    test_item = JSON.stringify(item);
    localStorage.setItem(item_id, test_item);
  }
  localStorage.setItem(item_id, item_stringify);
}

// removes all of an item from the cart
function remove_item(item_id){
  localStorage.removeItem(item_id);
}

// removes 1 of an item from the cart
function remove_item_one(item_id){
  var item = JSON.parse(localStorage.getItem(item_id));
  item.qty--;
}

// return: array of strings, every item (shopping_cart_item) in cart stringified
function get_cart(){
  var item = [];
  for (var i = 0; i < localStorage.length; i++) {
    item.push(localStorage.getItem(localStorage.key(i)));
  }
  return item;
}

// Send necessary information to cart_processing.py
function purchase(){
  // get cart information and make it a string
  var cart_items = JSON.stringify(get_cart());
  var username = document.getElementById('username')

  // send the information to cart_processing.py
  $.ajax({
    url: 'file',
    type: 'POST',
    data: {
      'username': username, 'cart': cart_items
    },
    success: function(data){
      // clean the cart
      clear_cart();
    },
    error: function(err){
      console.log(err.message);
    }
  });


}

// Erase everything in localstorage
// Call after a purchase
function clear_cart(){
  localStorage.clear();
}
