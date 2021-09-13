import json
import unittest

from sqlalchemy.exc import IntegrityError
from test_config import TestConfig
from vending_machine import bcrypt, create_app, init_db
from vending_machine.models import User

class TestRegister(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        self.get_response = self.client.get('/user/register')
        
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
    
    def test_register_route_get_response_is_application_json(self):
        self.assertEqual(self.get_response.content_type, 'application/json')
    
    def test_register_route_get_response_has_instructions_to_register(self):
        self.assertEqual(self.get_response.get_json()['message'], 
                         'Please send email, password and seller (bool) as a post request to /register. '\
                         'Set seller to False if you want to register as a buyer.')
    
    def test_register_new_user_as_buyer_added_to_db(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        with self.app.app_context():
            new_buyer = User.query.filter_by(username=self.post_data_buyer['username']).first()
            self.assertIsNotNone(new_buyer)
            self.assertEqual(new_buyer.username, self.post_data_buyer['username'])
    
    def test_register_new_user_as_seller_added_to_db(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        with self.app.app_context():
            new_seller = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertIsNotNone(new_seller)
            self.assertEqual(new_seller.role, 'seller')
    
    def test_register_new_user_success_response_message(self):
        response = self.client.post('/user/register', json=self.post_data_buyer)
        response_message = response.get_json()['message']
        self.assertEqual(response_message, 'registered successfully')
        
        response = self.client.post('/user/register', json=self.post_data_seller)
        response_message = response.get_json()['message']
        self.assertEqual(response_message, 'registered successfully')
    
    def test_username_should_be_unique(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        response = self.client.post('/user/register', json=self.post_data_buyer)
        self.assertEqual(response.get_json()['message'], 
                         'username already exists. Please register with a different one')
    
    def test_register_post_request_with_missing_username(self):
        post_data = {
            'password': 'password'
        }
        response = self.client.post('/user/register', json=post_data)
        self.assertEqual(response.get_json()['message'],
                    'username not provided')
    
    def test_register_post_request_with_missing_password(self):
        post_data = {
            'username': 'ronaldocr7'
        }
        response = self.client.post('/user/register', json=post_data)
        self.assertEqual(response.get_json()['message'],
                    'password not provided')
    
    def test_register_post_request_without_seller_registers_as_buyer(self):
        post_data = {
            'username': 'HaNuMaN',
            'password': 'jaishriram'
        }
        _ = self.client.post('/user/register', json=post_data)
        with self.app.app_context():
            test_user = User.query.filter_by(username=post_data['username']).first()
            self.assertEqual(test_user.role, 'buyer')
    
    def test_register_hashes_password_before_storing(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        with self.app.app_context():
            user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertTrue(bcrypt.check_password_hash(user.password, self.post_data_seller['password']))

class TestLogin(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_get_request_to_login_returns_instructions(self):
        response = self.client.get('/user/login')
        self.assertEqual(response.get_json()['message'], 
                         'please make valid post request with username and password')
    
    def test_successful_login_returns_success_message(self):
        register_data = {
            'username': 'candaceowens767',
            'password': 'Doofenshmirtz',
            'seller': True
        }
        login_data = {
            'username': 'candaceowens767',
            'password': 'Doofenshmirtz'
        }
        _ = self.client.post('/user/register', json=register_data)
        response = self.client.post('/user/login', json=login_data)
        self.assertEqual(response.get_json()['message'],
                         'login successful')
    
    def test_wrong_username_failed_login_returns_failure_message(self):
        register_data = {
            'username': 'phineas458',
            'password': 'pkdudeisawesome',
            'seller': False
        }
        login_data = {
            'username': 'doofenshmritzEvilInc',
            'password': 'pkdudeisawesome',
        }
        _ = self.client.post('/user/register', json=register_data)
        response = self.client.post('/user/login', json=login_data)
        self.assertEqual(response.get_json()['message'],
                         'login attempt failed due to incorrect username')
    
    def test_wrong_password_failed_login_returns_failure_message(self):
        register_data = {
            'username': 'phineas458',
            'password': 'pkdudeisawesome',
            'seller': True
        }
        login_data = {
            'username': 'phineas458',
            'password': 'udaydudeisawesome',
        }
        _ = self.client.post('/user/register', json=register_data)
        response = self.client.post('/user/login', json=login_data)
        self.assertEqual(response.get_json()['message'],
                         'login attempt failed due to incorrect password')
 
class TestLogout(unittest.TestCase):
    
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
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_get_request_to_logout_without_logging_in_returns_message(self):
        response = self.client.get('/user/logout')
        self.assertEqual(response.get_json()['message'], 'user not logged in')
    
    def test_get_request_to_logout_after_being_logged_in_returns_success_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        response = self.client.get('/user/logout')
        self.assertEqual(response.get_json()['message'],
                         'user logged out successfully')

class TestAccount(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        self.get_response = self.client.get('/user/register')
        
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
    
    def test_get_request_for_buyer_displays_account_data(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        response = self.client.get('/user/account')
        expected_response = {
            'username': self.post_data_buyer['username'],
            'deposit': 0.0,
            'role': 'buyer'
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_get_request_for_seller_displays_account_data(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        response = self.client.get('/user/account')
        expected_response = {
            'username': self.post_data_seller['username'],
            'deposit': 0.0,
            'role': 'seller'
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_patch_request_to_update_username(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        patch_data = {
            'username': 'theStig'
        }
        with self.app.app_context():
            user = User.query.filter_by(username=self.post_data_buyer['username']).first()
            response = self.client.patch('/user/account/update_username', json=patch_data)
            updated_user = User.query.filter_by(username=patch_data['username']).first()
            self.assertEqual(updated_user.id, user.id)
            self.assertEqual(response.get_json()['message'], 'username updated')
    
    def test_patch_request_to_update_username_must_be_unique(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        patch_data = {
            'username': self.post_data_seller['username']
        }
        response = self.client.patch('/user/account/update_username', json=patch_data)
        self.assertEqual(response.get_json()['message'],
                         'new username already exists. Please choose a different one.')
    
    def test_patch_request_to_update_password(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        patch_data = {
            'password': 'ThisIsTheNewPassword456'
        }
        with self.app.app_context():
            response = self.client.patch('/user/account/update_password', json=patch_data)
            updated_user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertTrue(bcrypt.check_password_hash(updated_user.password, patch_data['password']))
            self.assertEqual(response.get_json()['message'], 'password updated')

    def test_patch_request_to_update_role(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        patch_data = {
            'role': 'seller'
        }
        with self.app.app_context():
            response = self.client.patch('/user/account/update_role', json=patch_data)
            updated_user = User.query.filter_by(username=self.post_data_buyer['username']).first()
            self.assertEqual(updated_user.role, patch_data['role'])
            self.assertEqual(response.get_json()['message'], 'role updated')

    def test_delete_account_request_with_null_password_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        delete_data = {
            'password': None
        }
        response = self.client.delete('/user/account/delete', json=delete_data)
        self.assertEqual(response.get_json()['message'],
                         'Null password received. Account cannot be deleted without password confirmation.')
    
    def test_delete_account_request_with_empty_password_returns_failure_message(self):
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
        delete_data = {
            'password': ''
        }
        response = self.client.delete('/user/account/delete', json=delete_data)
        self.assertEqual(response.get_json()['message'],
                         'Empty password received. Account cannot be deleted without password confirmation.')

    def test_delete_account_given_incorrect_password(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        delete_data =  {
            'password': 'BillionsOfBlueBlisteringBarnacles'
        }
        response = self.client.delete('/user/account/delete', json=delete_data)
        self.assertEqual(response.get_json()['message'], 
                         'password incorrect. Please check and try again' )

    def test_delete_account_given_valid_password(self):
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        delete_data =  {
            'password': self.post_data_buyer['password']
        }
        response = self.client.delete('/user/account/delete', json=delete_data)
        self.assertEqual(response.get_json()['message'],
                         'user account deleted')
        with self.app.app_context():
            deleted_user = User.query.filter_by(username=self.post_data_buyer['username']).first()
            self.assertIsNone(deleted_user)

class TestRequestsIfLoggedIn(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        self.get_response = self.client.get('/user/register')
        
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

if __name__ == '__main__':
    unittest.main()
