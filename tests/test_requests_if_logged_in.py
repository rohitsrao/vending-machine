import unittest

from test_config import TestConfig
from vending_machine import create_app, init_db

class TestRequestsIfLoggedIn(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        
        self.post_data_buyer = {
            'username': 'hummuslover',
            'password': 'pw123',
            'seller': False
        }
        
        self.post_data_buyer_login = {
            'username': 'hummuslover',
            'password': 'pw123',
        }
        
        self.post_data_seller = {
            'username': 'pikachu',
            'password': 'password',
            'seller': True
        }
        
        self.post_data_seller_login = {
            'username': 'pikachu',
            'password': 'password',
        }
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_get_request_to_register_when_logged_in_returns_message(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        response = self.client.get('/user/register')
        self.assertEqual(response.get_json()['message'],
                         'user already logged in')
    
    def test_post_request_to_register_when_logged_in_returns_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        response = self.client.post('/user/register', json=self.post_data_seller)
        self.assertEqual(response.get_json()['message'],
                         'user already logged in')
    
    def test_get_request_to_login_when_logged_in_returns_message(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        response = self.client.get('/user/login')
        self.assertEqual(response.get_json()['message'],
                         'user already logged in')
    
    def test_put_request_to_login_when_logged_in_returns_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        response = self.client.post('/user/login', json=self.post_data_seller_login)
        self.assertEqual(response.get_json()['message'],
                         'user already logged in')
    
    def test_get_request_to_account_without_logging_returns_message(self):
        response = self.client.get('/user/account')
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to access this page')
    
    def test_patch_request_to_update_username_without_logging_in_returns_failure_message(self):
        patch_data = {
            'username': 'theStig'
        }
        response = self.client.patch('/user/account/update_username', json=patch_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to update username')
    
    def test_patch_request_to_update_username_without_logging_in_returns_failure_message(self):
        patch_data = {
            'password': 'ThisIsTheNewPassword456'
        }
        response = self.client.patch('/user/account/update_password', json=patch_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to update password')
    
    def test_patch_request_to_update_role_without_logging_in_returns_failure_message(self):
        patch_data = {
            'role': 'seller'
        }
        response = self.client.patch('/user/account/update_role', json=patch_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to update role')
    
    def test_delete_request_to_account_delete_without_logging_in_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        delete_data = {
            'password': self.post_data_seller['password']
        }
        response = self.client.delete('/user/account/delete', json=delete_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to delete account')

    def test_product_add_without_login_returns_failure_message(self):
        product_data = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to add a new product')

    def test_add_product_logged_in_as_buyer_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        product_data = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be a seller to add a new product')

    def test_put_request_without_logging_in_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        product_data = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100
        }
        _ = self.client.post('/product/add', json=product_data)
        _ = self.client.get('/user/logout')
        updated_product_data = {
            'productName': 'Coca Cola 0.5L',
            'amountAvailable': 20,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be logged in to update product')

    def test_put_request_as_buyer_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        product_data = {
            'productName': 'Coca Cola 0.3L',
            'amountAvailable': 10,
            'cost': 100
        }
        _ = self.client.post('/product/add', json=product_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        updated_product_data = {
            'productName': 'Coca Cola 0.5L',
            'amountAvailable': 20,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'user must be a seller to update product')

#if __name__ == '__main__':
#    unittest.main()
