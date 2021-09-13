from flask import current_app, jsonify, request
from flask import Blueprint
from flask_login import current_user

from vending_machine import db
from vending_machine.models import Product, User

product = Blueprint('product', __name__)

@product.route('/add', methods=['POST'])
def add_product():
    if current_user.is_authenticated:
        if current_user.role != 'seller':
            return jsonify(message='user must be a seller to add a new product')
        req = request.get_json()
        product_name = req['productName']
        amountAvailable = req['amountAvailable']
        cost = req['cost']
        seller = User.query.filter_by(username=current_user.username).first()
        product = Product(
            productName = product_name,
            amountAvailable = amountAvailable,
            cost = cost,
            seller = seller
        )
        with current_app.app_context():
            db.session.add(product)
            db.session.commit()
        return jsonify(message='product added')
    else:
        return jsonify(message='user must be logged in to add a new product')

@product.route('/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get(product_id)
    response_json = {
        'productName' : product.productName,
        'amountAvailable': product.amountAvailable,
        'cost': product.cost,
        'sellerId': product.sellerId
    }
    return jsonify(response_json)
