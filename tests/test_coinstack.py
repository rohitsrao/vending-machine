import unittest

from test_config import TestConfig
from vending_machine import create_app, db
from vending_machine.models import Coinstack, Product, User

class TestAppConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = db

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

if __name__ == '__main__':
    unittest.main()
