from flask import jsonify, current_app
from flask import Blueprint
from vending_machine.models import Product

main_page = Blueprint('main_page', __name__)


@main_page.route('/', methods=['GET'])
def home():
    products_dict = {}
    with current_app.app_context():
        products = Product.query.all()
        for product in products:
            d = {
                'productName': product.productName,
                'amountAvailable': product.amountAvailable,
                'cost': product.cost
            }
            products_dict[str(product.id)] = d
    return jsonify(
        products = products_dict
    )
