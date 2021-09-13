import unittest

from test_config import TestConfig
from vending_machine import create_app, init_db
from vending_machine.models import Product

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

if __name__ == '__main__':
    unittest.main()
