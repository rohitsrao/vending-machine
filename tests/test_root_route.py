import unittest

from vending_machine import app
from vending_machine import db

class TestRootRoute(unittest.TestCase):

    def test_root_route_response_is_application_json(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.content_type, 'application/json')
