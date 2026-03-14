import psycopg2
import os

connection = None

def get_sql_connection():
    global connection
    if connection is not None and not connection.closed:
        return connection
    
    print("Opening new PostgreSQL connection...")
    database_url = os.environ.get('DATABASE_URL')
    connection = psycopg2.connect(database_url)
    connection.autocommit = True
    print("Connection established.")
    return connection
