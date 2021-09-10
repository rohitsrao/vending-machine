from flask import jsonify
from vending_machine import app

@app.route('/', methods=['GET'])
def home():
    return jsonify(
        products = {}
    )
