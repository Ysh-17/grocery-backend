from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert main order
    order_query = (
        "INSERT INTO orders "
        "(customer_name, total, `datetime`) "
        "VALUES (%s, %s, %s)"
    )

    order_data = (
        order['customer_name'],
        order['total'],  
        datetime.now()
    )

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # Insert order details
    order_detail_query = (
        "INSERT INTO order_details "
        "(order_id, product_id, quantity, total_price) "
        "VALUES (%s, %s, %s, %s)"
    )

    order_details_data = [
        (
            order_id,
            int(item['product_id']),
            float(item['quantity']),
            float(item['total_price'])
        )
        for item in order['order_details']
    ]

    cursor.executemany(order_detail_query, order_details_data)
    connection.commit()

    cursor.close()
    return order_id


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = (
        "SELECT od.order_id, od.quantity, od.total_price, "
        "p.name, p.price_per_unit "
        "FROM order_details od "
        "LEFT JOIN products p ON od.product_id = p.product_id "
        "WHERE od.order_id = %s"
    )

    cursor.execute(query, (order_id,))

    records = []
    for (oid, quantity, total_price, name, price) in cursor:
        records.append({
            'order_id': oid,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': name,
            'price_per_unit': price
        })

    cursor.close()
    return records


def get_all_orders(connection):
    cursor = connection.cursor()

    query = "SELECT order_id, customer_name, total, `datetime` FROM orders"
    cursor.execute(query)

    orders = []
    for (order_id, customer_name, total, dt) in cursor:
        orders.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt
        })

    cursor.close()

    # Attach order details
    for order in orders:
        order['order_details'] = get_order_details(connection, order['order_id'])

    return orders


if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
