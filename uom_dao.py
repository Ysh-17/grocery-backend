def get_uoms(connection):
    cursor = connection.cursor()

    query = "SELECT uom_id, uom_name FROM uom"

    cursor.execute(query)

    response = []
    for row in cursor.fetchall():
        response.append({
            'uom_id': row[0],
            'uom_name': row[1]
        })

    cursor.close()
    return response

