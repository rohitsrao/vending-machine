import unittest

from test_config import TestConfig
from vending_machine import create_app, db
from vending_machine.models import Coinstack, Product, User

class TestCoinstack(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = db
        self.client = self.app.test_client()
        
        self.post_data_seller = {
            'username': 'seller1',
            'password': 'randomGibberish777',
            'role': 'seller'
        }
        
        self.post_data_seller_login = {
            'username': 'seller1',
            'password': 'randomGibberish777',
        }
        
        self.post_data_buyer = {
            'username': 'hummuslover',
            'password': 'pw123',
            'role': 'buyer'
        }
        
        self.post_data_buyer_login = {
            'username': 'hummuslover',
            'password': 'pw123',
        }
        
        self.product1_data = {
            'productName': 'product1',
            'amountAvailable': 10,
            'cost': 75
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
     
    def test_coinstack_updates_after_deposit_refund(self):
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
        response = self.client.get('/user/deposit/reset', json=deposit_data)
        change_returned = response.get_json()['change']
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            self.assertEqual(coinstack.c5, 40 + deposit_data['c5'] - change_returned['c5']*5)
            self.assertEqual(coinstack.c10, 40 + deposit_data['c10'] - change_returned['c10']*10)
            self.assertEqual(coinstack.c20, 40 + deposit_data['c20'] - change_returned['c20']*20)
            self.assertEqual(coinstack.c50, 40 + deposit_data['c50'] - change_returned['c50']*50)
            self.assertEqual(coinstack.c100, 40 + deposit_data['c100'] - change_returned['c100']*100)
     
    def test_coinstack_udpated_after_purchase(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 3,
            'c20': 0,
            'c50': 1,
            'c100': 0
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 1,
        }
        response = self.client.post('/product/buy', json=buy_data)
        change_returned = response.get_json()['change']
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            self.assertEqual(coinstack.c5, 40 + deposit_data['c5'] - change_returned['c5']*5)
            self.assertEqual(coinstack.c10, 40 + deposit_data['c10'] - change_returned['c10']*10)
            self.assertEqual(coinstack.c20, 40 + deposit_data['c20'] - change_returned['c20']*20)
            self.assertEqual(coinstack.c50, 40 + deposit_data['c50'] - change_returned['c50']*50)
            self.assertEqual(coinstack.c100, 40 + deposit_data['c100'] - change_returned['c100']*100)

if __name__ == '__main__':
    unittest.main()
