import unittest

from test_config import TestConfig
from vending_machine import create_app

class TestRootRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
     
    def test_root_route_response_is_application_json(self):
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'application/json')
     
    def test_get_response_contains_products(self):
        json_response = self.client.get('/').get_json()
        self.assertIn('products', json_response.keys())

if __name__ == '__main__':
    unittest.main()
