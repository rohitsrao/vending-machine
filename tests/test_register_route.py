import json
import unittest

from sqlalchemy.exc import IntegrityError
from test_config import TestConfig
from vending_machine import create_app, init_db
from vending_machine.models import User

class TestRegisterRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
        
        self.client = self.app.test_client()
        self.get_response = self.client.get('/register')
        
        self.post_data_buyer = {
            'username': 'hummuslover',
            'password': 'pw123',
            'seller': False
        }
        
        self.post_data_seller = {
            'username': 'pikachu',
            'password': 'password',
            'seller': True
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
        _ = self.client.post('/register', json=self.post_data_buyer)
        with self.app.app_context():
            new_buyer = User.query.filter_by(username=self.post_data_buyer['username']).first()
            self.assertIsNotNone(new_buyer)
            self.assertEqual(new_buyer.username, self.post_data_buyer['username'])
    
    def test_register_new_user_as_seller_added_to_db(self):
        _ = self.client.post('/register', json=self.post_data_seller)
        with self.app.app_context():
            new_seller = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertIsNotNone(new_seller)
            self.assertEqual(new_seller.role, 'seller')
    
    def test_register_new_user_success_response_message(self):
        response = self.client.post('/register', json=self.post_data_buyer)
        response_message = response.get_json()['message']
        self.assertEqual(response_message, 'registered successfully')
        
        response = self.client.post('/register', json=self.post_data_seller)
        response_message = response.get_json()['message']
        self.assertEqual(response_message, 'registered successfully')

    def test_username_should_be_unique(self):
        _ = self.client.post('/register', json=self.post_data_buyer)
        with self.assertRaises(IntegrityError):
            _ = self.client.post('/register', json=self.post_data_buyer)
