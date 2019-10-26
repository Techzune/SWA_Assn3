# name:   db.py
# author: Jordan Stremming
#
# Provides methods for database connection
#   also, creates database tables
#
import os
import sqlite3
from flask import g
from models import ItemCategory, Purchase, ShoppingCartItem, Address, ShoppingCart
from models import InventoryItem
from models import User

# database file location

DATABASE = "./data.db"


def create_db(force=False):
    """
    Automatically creates database, if needed.
    :param force: if True, creates the database anyways. NOTE: does not delete existing db. Renames
                    renames old database to DATABASE_FILE.db.old.
    """
    if force:
        try:
            print("attempting to archive existing database.")
            os.rename(DATABASE, DATABASE + ".old")
        except OSError as ose:
            print("error archiving database file:", ose)

    # if database does not exist, create tables
    if not os.path.exists(DATABASE) or force:
        db = sqlite3.connect("./data.db")
        cur = db.cursor()

        # create User table
        cur.execute("""
            CREATE TABLE User (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT,
                Password TEXT
            );
        """)
        # create InventoryItem table
        cur.execute("""
            CREATE TABLE InventoryItem (
                ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT,
                Description TEXT,
                Price FLOAT,
                Category TEXT,
                Quantity INTEGER
            );
        """)
        db.commit()
        # create Purchase table
        cur.execute("""
            CREATE TABLE Purchase (
                PurchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT,
                TotalPrice FLOAT,
                CreditCard TEXT,
                Address TEXT
            );
        """)
        db.commit()
        # create PurchaseItem table
        cur.execute("""
            CREATE TABLE PurchaseItem (
                PurchaseID INTEGER PRIMARY KEY,
                InventoryItemID INTEGER,
                Price FLOAT,
                Quantity INTEGER,
                FOREIGN KEY (PurchaseID) REFERENCES Purchase (PurchaseID),
                FOREIGN KEY (InventoryItemID) REFERENCES InventoryItem (ItemID)
            );
        """)
        db.commit()
        # create ShoppingCartItem table
        cur.execute("""
            CREATE TABLE ShoppingCartItem (
                UserID INTEGER,
                InventoryItemID INTEGER,
                Price FLOAT,
                Quantity INTEGER,
                FOREIGN KEY (UserID) REFERENCES User (UserID),
                FOREIGN KEY (InventoryItemID) REFERENCES InventoryItem (ItemID)
            );
        """)
        db.commit()

        # insert Admin user
        add_user(User(username="admin", password="password"), db)
        # insert Sample Inventory item
        cur.execute("""
            INSERT INTO InventoryItem (ItemName, Description, Price, Category) 
            VALUES ('Sample Item', 'Just your average item.', 10.00, 'TOYS');    
            """)

        db.commit()
        cur.close()
        db.close()


def get_db():
    """
    Gets the database connection.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("./data.db")
    return db


def add_user(user, db=None):
    """
    Adds a user to the database.

    :param user: User of user to insert
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO User (Username, Password) VALUES (?, ?)",
                [user.username, user.password])
    db.commit()
    cur.close()


def update_user_password(user, db=None):
    """
    Updates password for a User.
    If User does not exist, will Insert user.

    :param user: User of user to update
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("UPDATE User SET Password=? WHERE UserID=?",
                [user.password, user.id_])
    db.commit()
    cur.close()

    # if the update failed, insert it
    if cur.rowcount == 0:
        add_user(user, db)


def get_user(user, db=None):
    """
    Attempts to find a user with provided username and password.

    :param user: User of user to find
    :param db: optional, the database connection to commit to
    :return: User, if the user exists. Otherwise, None.
    """
    db = db or get_db()
    cur = db.cursor()

    query = "SELECT UserID, Username, Password FROM User "
    if user.id_ is not None:
        # Find by ID
        cur.execute(query + "WHERE UserID=?",
                    [user.id_])
    elif user.username is not None and user.password is None:
        # Find by Username
        cur.execute(query + "WHERE Username=?",
                    [user.username])
    else:
        # Find by Username and Password
        cur.execute(query + "WHERE Username=? AND Password=?",
                    [user.username, user.password])

    result = None
    row = cur.fetchone()
    if row is not None:
        # fetch the user
        result = User(id_=row[0], username=row[1], password=row[2])

    cur.close()
    return result


def get_inventory_item(item, db=None):
    """
    Gets a singular InventoryItem
    :param item: InventoryItem
    :param db: optional
    :return: InventoryItem
    """
    db = db or get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT ItemID, ItemName, Description, Price, Category, Quantity
        FROM InventoryItem
        WHERE ItemID=?   
    """, [item.id_])
    row = cur.fetchone()
    if row is not None:
        return InventoryItem(id_=row[0], name=row[1], description=row[2],
                             price=row[3], category=ItemCategory[row[4]], qty=row[5])
    return None


def get_inventory(db=None):
    """
    Gets all InventoryItems.

    :param db: optional, the database connection to commit to
    :returns: list, all items in Inventory as InventoryItems
    """
    db = db or get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT ItemID, ItemName, Description, Price, Category, Quantity
        FROM InventoryItem    
    """)

    result = []
    for row in cur.fetchall():
        try:
            if row[5] > 0:
                result.append(InventoryItem(id_=row[0], name=row[1], description=row[2],
                                            price=row[3], category=ItemCategory[row[4]], qty=row[5]))
        except Exception as e:
            print("invalid inventory item:", e)

    cur.close()
    return result


def add_item(item, db=None):
    """
    Adds an InventoryItem to the database.

    :param item: InventoryItem to insert
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO InventoryItem (ItemName, Description, Price, Category, Quantity) 
        VALUES (?, ?, ?, ?, ?)
    """, [item.name, item.description, item.price, str(item.category), item.quantity])
    db.commit()

    cur.close()


def add_to_cart(user, item, qty=1, db=None):
    """
    Adds an InventoryItem to user's shopping cart.

    :param user: User
    :param item: InventoryItem to insert
    :param qty: int, quantity to insert
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE ShoppingCartItem
           SET Quantity = Quantity + ?
         WHERE UserID=?
           AND InventoryItemID=?
    """, [qty, user.id_, item.id_])

    if cur.rowcount == 0:
        cur.execute("""
            INSERT INTO ShoppingCartItem (UserID, InventoryItemID, Price, Quantity)
            VALUES (?, ?, ?, ?)
        """, [user.id_, item.id_, item.price, qty])

    db.commit()
    cur.close()


def remove_from_cart(user, item, qty=1, db=None):
    """
    Removes a ShoppingCartItem from user's shopping cart.

    :param user: User
    :param item: ShoppingCartItem to remove
    :param qty: int, quantity to remove
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE ShoppingCartItem
           SET Quantity = Quantity - ?
         WHERE UserID=?
           AND InventoryItemID=?
    """, [qty, user.id_, item.item.id_])
    cur.execute("""
        DELETE FROM ShoppingCartItem
        WHERE Quantity < 1
    """)
    db.commit()
    cur.close()


def update_item(item, db=None):
    """
    Updates attributes for an InventoryItem.
    If InventoryItem does not exist, inserts instead.

    :param item: InventoryItem to update
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE InventoryItem
        SET ItemName = ?,
            Description = ?,
            Price = ?,
            Category = ?,
            Quantity = ?
        WHERE ItemID = ? 
    """, [item.name, item.description, item.price, str(item.category), item.quantity, item.id_])
    db.commit()
    cur.close()

    # if the update failed, insert it
    if cur.rowcount == 0:
        add_item(item, db)


def get_shopping_cart(user, db=None):
    """
    Gets all ShoppingCartItems for user

    :param user: User, the user to request for
    :param db: optional, the database connection
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT InventoryItemID, Price, Quantity
        FROM ShoppingCartItem
        WHERE UserID = ?
    """, [user.id_])

    cart = ShoppingCart(user)
    for row in cur.fetchall():
        try:
            item = get_inventory_item(InventoryItem(id_=row[0]), db)
            cart.items.append(ShoppingCartItem(item=item, price=row[1], qty=row[2]))
        except Exception as e:
            print("invalid purchase item:", e)

    cur.close()
    return cart


def get_purchase(purchase, db=None):
    """
    Gets a purchase from the database based on PurchaseID

    :param purchase: Purchase, must have id
    :param db: optional, the database connection
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT Username, TotalPrice, CreditCard, Address
        FROM Purchase
        WHERE PurchaseID = ?
    """, [purchase.id_])

    row = cur.fetchone()
    try:
        purchase = Purchase(id_=purchase.id_, username=row[0], total_price=row[1],
                            credit_card=row[2], address=Address().from_str(row[3]))
    except Exception as e:
        print("invalid purchase:", e)

    cur.execute("""
        SELECT InventoryItemID, Price, Quantity
        FROM PurchaseItem
        WHERE pi.PurchaseID = ?
    """, [purchase.id_])

    for row in cur.fetchall():
        try:
            item = get_inventory_item(InventoryItem(id_=row[0]), db)
            purchase.items.append(ShoppingCartItem(item=item, price=row[1], qty=row[2]))
        except Exception as e:
            print("invalid purchase item:", e)

    cur.close()
    return purchase


def add_purchase(purchase, db=None):
    """
    Inserts a purchase into the database.

    :param purchase: Purchase, what to insert
    :param db: optional, the database connection
    """
    db = db or get_db()
    cur = db.cursor()

    # insert the purchase
    cur.execute("""
        INSERT INTO Purchase (Username, TotalPrice, CreditCard, Address) 
        VALUES (?, ?, ?, ?)    
    """, [purchase.username, purchase.total_price, purchase.credit_card, purchase.address.to_str()])
    purchase.id_ = cur.lastrowid

    # insert all the items for the purchase
    for item in purchase.items:
        cur.execute("""
            INSERT INTO PurchaseItem (PurchaseID, InventoryItemID, Price, Quantity) 
            VALUES (?, ?, ?, ?)
        """, [purchase.id_, item.item_id, item.qty, item.price])

    db.commit()
    cur.close()
