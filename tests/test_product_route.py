import unittest

from test_config import TestConfig
from vending_machine import create_app, init_db
from vending_machine.models import Product, User

class TestProductRoute(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        
        self.post_data_seller = {
            'username': 'pikachu',
            'password': 'password',
            'seller': True
        }
        
        self.post_data_seller_login = {
            'username': 'pikachu',
            'password': 'password',
        }
        
        self.product_data = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100
        }
        
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_add_product_to_db(self):
        response = self.client.post('/product/add', json=self.product_data)
        self.assertEqual(response.get_json()['message'],
                         'product added')
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            self.assertIsNotNone(product)
    
    def test_add_product_has_current_seller_id(self):
        response = self.client.post('/product/add', json=self.product_data)
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertEqual(product.sellerId, user.id)
    
    def test_added_product_shows_up_under_user_products_sold(self):
        response = self.client.post('/product/add', json=self.product_data)
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertTrue(product in user.products_sold)
    
    def test_view_product_details_given_valid_product_id(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.get('/product/1')
        expected_response = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100,
            'sellerId': 1
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_view_product_details_given_invalid_product_id_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.get('/product/2')
        self.assertEqual(response.get_json()['message'],
                         'invalid product id. Please check and try again.')
    
    def test_put_request_to_update_product_details(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Coca Cola 0.5L',
            'amountAvailable': 20,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'product details updated')
        with self.app.app_context():
            product = Product.query.get(1)
            self.assertEqual(product.productName, updated_product_data['productName'])
            self.assertEqual(product.amountAvailable, updated_product_data['amountAvailable'])
            self.assertEqual(product.cost, updated_product_data['cost'])

if __name__ == '__main__':
    unittest.main()