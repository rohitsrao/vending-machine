import unittest

from vending_machine import create_app
from vending_machine.models import Product

class TestRootRoute(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
    
    def test_root_route_response_is_application_json(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.content_type, 'application/json')
    
    def test_get_response_contains_products(self):
        with self.app.test_client() as client:
            response = client.get('/')
            json_response = response.get_json()
            self.assertIn('products', json_response.keys())
