import mysql.connector
from mysql.connector import Error

def get_sql_connection():
    print("Opening MySQL connection")

    try:
        connection = mysql.connector.connect(
            host='sql12.freesqldatabase.com',
            user='sql12810410',
            password='WmIEWQ9xBg',
            database='sql12810410',
            port=3306,
            connection_timeout=30
        )

        if connection.is_connected():
            print("Connection successful")
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
