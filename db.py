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
        add_user("admin", "password", db)
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


def add_user(username, password, db=None):
    """
    Adds a user to the database.

    :param username: String of username
    :param password: String of password
    :param db: optional, the database connection to commit to
    """
    db = db or get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO User (Username, Password) VALUES (?, ?)",
                [username, password])
    db.commit()


def verify_user(username, password):
    """
    Attempts to find a user with provided username and password.

    :param username: String of username
    :param password: String of password
    :return: True, if the user exists.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM User WHERE Username=? AND Password=?",
                [username, password])
    result = cur.rowcount() > 0
    cur.close()
    return result

