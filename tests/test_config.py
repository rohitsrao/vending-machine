import unittest

from vending_machine import app

class TestRootRoute(unittest.TestCase):

    def test_app_config_SQLALCHEMY_DATABASE_URI_is_sqlite(self):
        with app.test_client() as client:
            self.assertIn('sqlite', app.config['SQLALCHEMY_DATABASE_URI'])
     
    def test_app_config_SQLALCHEMY_TRACK_MODIFICATIONS_is_False(self):
        with app.test_client() as client:
            self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
