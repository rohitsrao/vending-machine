import unittest

from vending_machine import db

class TestRootRoute(unittest.TestCase):

    def test_db_not_none(self):
        self.assertIsNotNone(db)
        self.assertIsNotNone(db.app)
