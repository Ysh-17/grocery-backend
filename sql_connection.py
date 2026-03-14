import psycopg2

connection = None

def get_sql_connection():
    global connection
    if connection is not None and not connection.closed:
        return connection
    
    print("Opening new PostgreSQL connection...")
    connection = psycopg2.connect(
        host='aws-1-ap-south-1.pooler.supabase.com',
        user='postgres.yoblktyuymaqboyzvrxb',
        password='Grocerystore@22',
        database='postgres',
        port=5432
    )
    connection.autocommit = True
    print("Connection established.")
    return connection
