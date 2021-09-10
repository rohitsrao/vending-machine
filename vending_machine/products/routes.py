from flask import jsonify
from flask import Blueprint

products = Blueprint('products', __name__)

@products.route('/', methods=['GET'])
def home():
    return jsonify(
        products = {}
    )
