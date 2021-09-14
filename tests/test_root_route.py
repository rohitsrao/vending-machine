import unittest

from test_config import TestConfig
from vending_machine import create_app, db

class TestRootRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.db = db
     
    def test_root_route_response_is_application_json(self):
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'application/json')
     
    def test_get_response_contains_products(self):
        json_response = self.client.get('/').get_json()
        self.assertIn('products', json_response.keys())

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_home_page_displays_3_products_from_database(self):
        self.post_data_seller = {
            'username': 'seller1',
            'password': 'randomGibberish777',
            'role': 'seller'
        }
        
        self.post_data_seller_login = {
            'username': 'seller1',
            'password': 'randomGibberish777',
        }
        
        self.product1_data = {
            'productName': 'product1',
            'amountAvailable': 10,
            'cost': 75
        }
        
        self.product2_data = {
            'productName': 'product2',
            'amountAvailable': 5,
            'cost': 150
        }
        
        self.product3_data = {
            'productName': 'product3',
            'amountAvailable': 15,
            'cost': 55
        }

        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.post('/product/add', json=self.product2_data)
        _ = self.client.post('/product/add', json=self.product3_data)
        _ = self.client.get('/user/logout')
        response = self.client.get('/')
        expected_response = {
            "1": {
                'productName': 'product1',
                'amountAvailable': 10,
                'cost': 75
            },
            "2": {
                'productName': 'product2',
                'amountAvailable': 5,
                'cost': 150
            },
            "3": {
                'productName': 'product3',
                'amountAvailable': 15,
                'cost': 55
            }
        }
        print(response.get_json()['products'])
        print(expected_response)
        self.assertEqual(response.get_json()['products'], expected_response)


if __name__ == '__main__':
    unittest.main()
