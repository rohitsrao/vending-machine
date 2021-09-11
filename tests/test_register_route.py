import unittest

from test_config import TestConfig
from vending_machine import create_app

class TestRegisterRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.response = self.client.get('/register')
    
    def test_register_route_get_response_is_application_json(self):
        self.assertEqual(self.response.content_type, 'application/json')
    
    def test_register_route_get_response_has_instructions_to_register(self):
        self.assertEqual(self.response.get_json()['message'], 
                         'Please send email, password, confirm_password as a post request to /register')
