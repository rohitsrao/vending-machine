from flask import jsonify
from vending_machine import app

@app.route('/')
def home():
    return jsonify('test')
