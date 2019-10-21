# name:   db.py
# author: Jordan Stremming
#
# Provides methods for database connection
#   also, creates database tables
#
import os
import sqlite3

from flask import g
from app import app
from model.user import User

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
                Category TEXT
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


@app.teardown_appcontext
def close_connection(_):
    """
    Automatically closes the connection for the database when app
    shuts down.

    :param _: unused parameter
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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


def verify_user(user, db=None):
    """
    Attempts to find a user with provided username and password.

    :param user: User of user to find
    :param db: optional, the database connection to commit to
    :return: User, if the user exists. Otherwise, None.
    """
    db = db or get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT UserID, Username, Password 
            FROM User 
            WHERE Username=? AND Password=?
        """, [user.username, user.password])

    result = None
    if cur.rowcount != 0:
        # fetch the user
        row = cur.fetchone()
        result = User(id_=row[0], username=row[1], password=row[2])

    cur.close()
    return result
