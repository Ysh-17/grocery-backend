from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sql_connection import get_sql_connection
import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)
CORS(app)

def get_connection():
    return get_sql_connection()

@app.route("/")
def home():
    return "Flask backend running successfully!"

@app.route('/getUOM', methods=['GET'])
def get_uom():
    connection = get_connection()
    return jsonify(uom_dao.get_uoms(connection))

@app.route('/getProducts', methods=['GET'])
def get_products():
    connection = get_connection()
    return jsonify(products_dao.get_all_products(connection))

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    try:
        connection = get_connection()
        payload = request.get_json()
        print("Received product:", payload)
        product_id = products_dao.insert_new_product(connection, payload)
        return jsonify({'product_id': product_id})
    except Exception as e:
        print("Insert error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    connection = get_connection()
    return jsonify(orders_dao.get_all_orders(connection))

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        connection = get_connection()
        payload = request.get_json()
        print("Received order:", payload)
        order_id = orders_dao.insert_order(connection, payload)
        return jsonify({'order_id': order_id})
    except Exception as e:
        print("Order insert error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    try:
        connection = get_connection()
        payload = request.get_json()
        product_id = payload.get("product_id")
        return_id = products_dao.delete_product(connection, product_id)
        return jsonify({'product_id': return_id})
    except Exception as e:
        print("Delete error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
