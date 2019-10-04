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

# if database does not exist, create tables
if not os.path.exists(DATABASE):
    conn = sqlite3.connect("./data.db")
    cur = conn.cursor()

    # create USER table
    cur.execute("""
        CREATE TABLE User (
            Username TEXT,
            Password TEXT
        );
    """)
    conn.commit()

    # insert ADMIN user
    cur.execute("""
        INSERT INTO User (Username, Password) 
            VALUES ('admin', 'admin');    
    """)
    conn.commit()
    conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("./data.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
