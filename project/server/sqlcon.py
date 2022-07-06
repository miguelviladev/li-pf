import sqlite3
from config import *

def connection():
    try:
        return sqlite3.connect(STORAGE_DB)
    except sqlite3.Error as error:
        raise Exception("Error connecting to the database: ", error)

def select(query):
    try:
        connection = connection()
        cursor = connection.cursor()
        cursor.execute(query)
        data =  cur.fetchall()
    except sqlite3.Error as error:
        raise Exception("Error executing query: ", error)
    finally:
        if connection: connection.close()
    return data

def execute(query):
    try:
        connection = connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as error:
        raise Exception("Error executing querry: ", error)
    finally:
        if connection: connection.close()