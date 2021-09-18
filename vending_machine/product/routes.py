from flask import current_app, jsonify, request
from flask import Blueprint
from flask_login import current_user
from sqlalchemy.orm import sessionmaker

from vending_machine import db
from vending_machine.helper_functions import *
from vending_machine.models import Coinstack, Product, User
from vending_machine.product.validation import *

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
        productName_is_invalid, error_message = validate_productName_when_adding_product(product_name)
        if productName_is_invalid: return jsonify(message=error_message)
        amountAvailable_is_invalid, error_message = validate_amountAvailable(amountAvailable)
        if amountAvailable_is_invalid: return jsonify(message=error_message)
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
    else: return jsonify(message='user must be logged in to add a new product')

@product.route('/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        response_json = {
            'productName' : product.productName,
            'amountAvailable': product.amountAvailable,
            'cost': product.cost,
            'sellerId': product.sellerId
        }
        return jsonify(response_json)
    else: return jsonify(message='invalid product id. Please check and try again.')

@product.route('/<int:product_id>/update', methods=['PUT'])
def update_product_details(product_id):
    if current_user.is_authenticated:
        if current_user.role != 'seller':
            return jsonify(message='user must be a seller to update product')
        req = request.get_json()
        product = Product.query.get(product_id)
        if current_user.id != product.sellerId:
            return jsonify(message='seller id of current user does not match seller id of product')
        productName_is_invalid, error_message = validate_productName_during_update(req['productName'])
        if productName_is_invalid: return jsonify(message=error_message)
        amountAvailable_is_invalid, error_message = validate_amountAvailable(req['amountAvailable'])
        if amountAvailable_is_invalid: return jsonify(message=error_message)
        with current_app.app_context():
            product.productName = req['productName']
            product.amountAvailable = req['amountAvailable']
            product.cost = req['cost']
            db.session.commit()
        return jsonify(message='product details updated')
    else: return jsonify(message='user must be logged in to update product')

@product.route('/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    if current_user.is_authenticated:
        if current_user.role != 'seller':
            return jsonify(message='user must be a seller to delete product')
        product = Product.query.get(product_id)
        if current_user.id != product.sellerId:
            return jsonify(message='seller id of current user does not match seller id of product')
        with current_app.app_context():
            db.session.delete(product)
            db.session.commit()
        return jsonify(message='product deleted')
    else: return jsonify(message='user must be logged in to delete product')

@product.route('/buy', methods=['POST'])
def buy_product():
    if current_user.is_authenticated:
        if current_user.role != 'buyer':
            return jsonify(message='user must be a buyer to buy')
        else:
            req = request.get_json()
            productId = req['productId']
            amountToBuy = req['amountToBuy']
            with current_app.app_context():
                user = User.query.get(current_user.id)
                product = Product.query.get(productId)
                if product is None: return jsonify(message='product id is invalid')
                if amountToBuy > product.amountAvailable: 
                    return jsonify(message='quantity requested to buy more than amount available')
                coinstack = Coinstack.query.get(1)
                product.amountAvailable -= amountToBuy
                total_cost = product.cost * amountToBuy
                if user.deposit < total_cost: 
                    return jsonify(message='insufficient or no deposit. Please deposit sufficient money and try again')
                change_amount = user.deposit - total_cost
                num_coins_available = format_num_coins_available(coinstack)
                change_coins = coin_change_calculator(change_amount, num_coins_available)
                if change_coins is None:
                    return jsonify(message='vending machine has insufficient change. Please contact customer service')
                reduce_change_from_coinstack(coinstack, change_coins)
                user.deposit = 0
                db.session.commit()
            return jsonify({
                'productPurchased': product.productName,
                'amountSpent': total_cost,
                'change': change_coins
            })
    else:
        return jsonify(message='user must be logged in to buy')
