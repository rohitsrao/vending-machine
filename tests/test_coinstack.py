import unittest

from test_config import TestConfig
from vending_machine import create_app, db
from vending_machine.models import Coinstack, Product, User

class TestCoinstack(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = db
        self.client = self.app.test_client()
    
        self.post_data_buyer = {
            'username': 'hummuslover',
            'password': 'pw123',
            'role': 'buyer'
        }
        
        self.post_data_buyer_login = {
            'username': 'hummuslover',
            'password': 'pw123',
        }
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_coinstack_table_exists(self):
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            self.assertIsNotNone(coinstack)
    
    def test_coinstack_default_values(self):
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            self.assertEqual(coinstack.__repr__(),
                            "Coinstack(5c: '40', 10c: '40', 20c: '40', 50c: '40', 100c: '40')")
    
    def test_coinstack_after_successful_deposit_updates_values(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 5,
            'c10': 4,
            'c20': 3,
            'c50': 2,
            'c100': 1
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            self.assertEqual(coinstack.__repr__(),
                            "Coinstack(5c: '45', 10c: '44', 20c: '43', 50c: '42', 100c: '41')")

if __name__ == '__main__':
    unittest.main()
