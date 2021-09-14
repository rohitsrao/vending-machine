import unittest

from test_config import TestConfig
from vending_machine import create_app, init_db
from vending_machine.models import Coinstack, Product, User

class TestUserModel(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_User_model_has_attributes(self):
        self.assertTrue(hasattr(User, 'username'))
        self.assertTrue(hasattr(User, 'password'))
        self.assertTrue(hasattr(User, 'deposit'))
        self.assertTrue(hasattr(User, 'role'))
    
    def test_User_repr_output_format(self):
        test_user = User(username='test_user', password='testpw123', deposit=0, role='buyer')
        self.assertEqual(test_user.__repr__(), "User('test_user', 0, 'buyer')")
    
    def test_User_created_with_default_float_zero_deposit(self):
        test_user = User(username='piakchu', password='&%!opkdfUI8', role='buyer')
        with self.app.app_context():
            self.db.session.add(test_user)
            self.db.session.commit()
            user_db = User.query.filter_by(username=test_user.username).first()
            self.assertEqual(user_db.deposit, 0.0)
            self.assertIsInstance(user_db.deposit, float)
    
    def test_user_created_with_default_buyer_role(self):
        test_user = User(username='Göthe', password='44444')
        with self.app.app_context():
            self.db.session.add(test_user)
            self.db.session.commit()
            user_db = User.query.filter_by(username=test_user.username).first()
            self.assertEqual(user_db.role, 'buyer')

class TestProductModel(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_Product_model_has_attribute(self):
        self.assertTrue(hasattr(Product, 'amountAvailable'))
        self.assertTrue(hasattr(Product, 'cost'))
        self.assertTrue(hasattr(Product, 'productName'))
        self.assertTrue(hasattr(Product, 'sellerId'))
    
    def test_Product_repr_output_format(self):
        test_user = User(username='test_user', password='testpw123', deposit=0, role='buyer')
        with self.app.app_context():
            self.db.session.add(test_user)
            self.db.session.commit()
            test_product = Product(productName='KitKat', amountAvailable=3, cost=4.75, sellerId=test_user.id)
            self.assertEqual(test_product.__repr__(), "Product('KitKat', 3, 4.75, 1)")
    
    def test_product_creation(self):
        test_user = User(username='piakchu', password='&%!opkdfUI8', role='buyer')
        with self.app.app_context():
            self.db.session.add(test_user)
            self.db.session.commit()
        test_product = Product(productName='product1', amountAvailable='5', cost=80, sellerId=1)
        with self.app.app_context():
            self.db.session.add(test_product)
            self.db.session.commit()
            product_in_db = Product.query.filter_by(productName=test_product.productName).first()
            self.assertIsNotNone(product_in_db)
            self.assertEqual(product_in_db.cost, 80)


class TestCoinStackModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = init_db(self.app)
        with self.app.app_context():
            self.db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_CoinStack_model_has_attributes(self):
        self.assertTrue(hasattr(Coinstack, 'c5'))
        self.assertTrue(hasattr(Coinstack, 'c10'))
        self.assertTrue(hasattr(Coinstack, 'c20'))
        self.assertTrue(hasattr(Coinstack, 'c50'))
        self.assertTrue(hasattr(Coinstack, 'c100'))
    
    def test_Coinstack_repr_output_format(self):
        test_stack = Coinstack(c5=1, c10=1, c20=1, c50=1, c100=1)
        self.assertEqual(test_stack.__repr__(), 
                         "Coinstack(5c: '1', 10c: '1', 20c: '1', 50c: '1', 100c: '1')")
    
    def test_Coinstack_default_value(self):
        test_stack = Coinstack()
        with self.app.app_context():
            self.db.session.add(test_stack)
            stack_db = Coinstack.query.get(1)
            self.assertEqual(stack_db.__repr__(), 
                            "Coinstack(5c: '40', 10c: '40', 20c: '40', 50c: '40', 100c: '40')")


if __name__ == '__main__':
    unittest.main()
