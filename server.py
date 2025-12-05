from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

from sql_connection import get_sql_connection   # Old connection restored

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)
CORS(app)

# ---------------------------------------
# Create MySQL connection (global usage)
# ---------------------------------------
connection = get_sql_connection()


@app.route("/")
def home():
    return "Flask backend running successfully!"


# ---------------------------------------
# UOM LIST
# ---------------------------------------
@app.route('/getUOM', methods=['GET'])
def get_uom():
    return jsonify(uom_dao.get_uoms(connection))


# ---------------------------------------
# PRODUCTS LIST
# ---------------------------------------
@app.route('/getProducts', methods=['GET'])
def get_products():
    return jsonify(products_dao.get_all_products(connection))


# ---------------------------------------
# INSERT PRODUCT  **FIXED**
# ---------------------------------------
@app.route('/insertProduct', methods=['POST'])
def insert_product():
    try:
        payload = request.get_json()
        print("Received product:", payload)

        product_id = products_dao.insert_new_product(connection, payload)
        return jsonify({'product_id': product_id})

    except Exception as e:
        print("Insert error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------------------------------
# GET ALL ORDERS
# ---------------------------------------
@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    return jsonify(orders_dao.get_all_orders(connection))


# ---------------------------------------
# INSERT ORDER
# ---------------------------------------
@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        payload = request.get_json()
        print("Received order:", payload)

        order_id = orders_dao.insert_order(connection, payload)
        return jsonify({'order_id': order_id})

    except Exception as e:
        print("Order insert error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------------------------------
# DELETE PRODUCT
# ---------------------------------------
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    try:
        payload = request.get_json()
        product_id = payload.get("product_id")

        return_id = products_dao.delete_product(connection, product_id)
        return jsonify({'product_id': return_id})

    except Exception as e:
        print("Delete error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------------------------------
# RUN SERVER (Waitress)
# ---------------------------------------
if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

