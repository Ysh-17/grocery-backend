import mysql.connector
from mysql.connector import Error
import time

connection = None

def get_sql_connection():
    global connection

    # If a connection exists, verify it's alive
    if connection is not None and connection.is_connected():
        try:
            connection.ping(reconnect=True, attempts=3, delay=2)
            return connection
        except:
            pass  # connection failed; reconnect below

    print("Opening new MySQL connection...")

    try:
        connection = mysql.connector.connect(
            host='sql12.freesqldatabase.com',
            user='sql12810410',
            password='WmIEWQ9xBg',
            database='sql12810410',
            port=3306,
            connection_timeout=30,
            autocommit=True,        # prevents idle-lock issues
            pool_name="mypool",     # enables internal pooling
            pool_size=5             # keeps multiple connections alive
        )

        if connection.is_connected():
            print("Connection established.")
            return connection

    except Error as e:
        print("Error while connecting:", e)
        return None


# OPTIONAL: background keep-alive thread
import threading

def keep_alive():
    global connection
    while True:
        if connection is not None:
            try:
                connection.ping(reconnect=True, attempts=3, delay=2)
            except:
                print("Keep-alive reconnecting...")
                get_sql_connection()

        time.sleep(60)  # ping server every 60 seconds


# Start keep-alive thread
threading.Thread(target=keep_alive, daemon=True).start()

