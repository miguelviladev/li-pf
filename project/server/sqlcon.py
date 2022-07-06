import os
import sqlite3
from config import *

def initializeDatabase():
    try:
        if not(os.path.exists(STORAGE_DB)):
            connection = sqlite3.connect(STORAGE_DB)
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    ownerships TEXT,
                    access_token TEXT,
                    expiration INTEGER)""")
            cursor.execute("""CREATE TABLE images (
                    identifier TEXT PRIMARY KEY,
                    nomen TEXT,
                    original_path TEXT,
                    protected_path TEXT,
                    owner TEXT,
                    collection TEXT,
                    history TEXT)
            """)
            connection.commit()
            connection.close()
    except sqlite3.Error as error:
        raise Exception("Error connecting to the database: ", error)

def selector(query, tupledata=None):
    connection = sqlite3.connect(STORAGE_DB)
    cursor = connection.cursor()
    cursor.execute(query, tupledata)
    data =  cursor.fetchall()
    connection.close()
    return data

def executor(query, tupledata=None):
    connection = sqlite3.connect(STORAGE_DB)
    cursor = connection.cursor()
    cursor.execute(query, tupledata)
    connection.commit()
    connection.close()