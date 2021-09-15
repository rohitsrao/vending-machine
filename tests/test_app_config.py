import unittest

from test_config import TestConfig
from vending_machine import create_app, db

class TestAppConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = db
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_app_config_SQLALCHEMY_DATABASE_URI_is_sqlite(self):
        with self.app.test_client() as client:
            self.assertIn('sqlite', self.app.config['SQLALCHEMY_DATABASE_URI'])
    
    def test_app_config_SQLALCHEMY_TRACK_MODIFICATIONS_is_False(self):
        with self.app.test_client() as client:
            print(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
            self.assertEqual(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)

if __name__ == '__main__':
    unittest.main()
