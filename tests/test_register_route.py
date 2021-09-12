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
                         'Please send email, password, confirm_password and seller (bool) as a post request to /register. '\
                         'default seller is set to false i.e default role is a buyer')
    
    def test_register_route_post_register_new_user(self):
        post_data = {
            "username": 'hummuslover',
            "password": 'pw123',
            "confirm_password": 'pw123',
        }
        response = self.client.post('/register', json=post_data)
        with self.app.app_context():
            self.db.create_all()
            new_user = User.query.filter_by(username=post_data["username"]).first()
            self.assertIsNotNone(new_user)
            self.assertEqual(new_user.username, post_data['username'])
