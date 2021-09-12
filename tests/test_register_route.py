import json
import unittest

from test_config import TestConfig
from vending_machine import create_app, init_db
from vending_machine.models import User

class TestRegisterRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = init_db(self.app)
        self.client = self.app.test_client()
        self.get_response = self.client.get('/register')
    
    def test_register_route_get_response_is_application_json(self):
        self.assertEqual(self.get_response.content_type, 'application/json')
    
    def test_register_route_get_response_has_instructions_to_register(self):
        self.assertEqual(self.get_response.get_json()['message'], 
                         'Please send email, password and seller (bool) as a post request to /register. '\
                         'Set seller to False if you want to register as a buyer.')
    
    def test_register_new_user_as_buyer(self):
        post_data = {
            "username": 'hummuslover',
            "password": 'pw123',
            "seller": False
        }
        response = self.client.post('/register', json=post_data)
        response_message = response.get_json()['message']
        with self.app.app_context():
            self.db.create_all()
            new_user = User.query.filter_by(username=post_data["username"]).first()
            self.assertIsNotNone(new_user)
            self.assertEqual(new_user.username, post_data['username'])
        self.assertEqual(response_message, 'registered successfully')

    def test_register_new_user_as_seller(self):
        post_data = {
            'username': 'pikachu',
            'password': 'password',
        }

