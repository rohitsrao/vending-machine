import unittest

from test_config import TestConfig
from vending_machine import create_app, db
from vending_machine.models import Coinstack, Product, User

class TestProductRoute(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = db
        
        self.client = self.app.test_client()
        
        self.post_data_seller = {
            'username': 'pikachu',
            'password': 'password',
            'role': 'seller'
        }
        
        self.post_data_seller_login = {
            'username': 'pikachu',
            'password': 'password',
        }
        
        self.product_data = {
            'productName': 'Water',
            'amountAvailable': 10,
            'cost': 100
        }
        
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_add_product_to_db(self):
        response = self.client.post('/product/add', json=self.product_data)
        self.assertEqual(response.get_json()['message'],
                         'product added')
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            self.assertIsNotNone(product)
    
    def test_productName_must_be_unique_when_adding_to_database(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.post('/product/add', json=self.product_data)
        self.assertEqual(response.get_json()['message'], 
                         'productName already exists')
    
    def test_adding_product_with_productName_longer_than_32_characters_returns_error_message(self):
        product_data = {
            'productName': 'this product name is longer than 32 characters',
            'amountAvailable': 10,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'productName must be shorter than 32 characters')
    
    def test_adding_product_with_None_productName_returns_error_message(self):
        product_data = {
            'productName': None,
            'amountAvailable': 10,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'productName cannot be None')
    
    def test_adding_product_with_amountAvailable_greater_than_15_returns_error_message(self):
        product_data = {
            'productName': 'Alive Water',
            'amountAvailable': 17,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'amountAvailable must be lesser than or equal to 15')
    
    def test_adding_product_with_negative_amountAvailable_returns_error_message(self):
        product_data = {
            'productName': 'Crystal Water',
            'amountAvailable': -5,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'amountAvailable must be positive')
    
    def test_adding_product_with_None_amountAvailable_returns_error_message(self):
        product_data = {
            'productName': 'Crystal Water',
            'amountAvailable': None,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'amountAvailable must not be None')
    
    def test_adding_product_with_non_int_amountAvailable_returns_error_message(self):
        product_data = {
            'productName': 'Crystal Water',
            'amountAvailable': 3.1415,
            'cost': 75
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'amountAvailable must be of type int')
    
    def test_adding_product_with_cost_not_a_multiple_of_5_returns_error(self):
        product_data = {
            'productName': 'Crystal Water',
            'amountAvailable': 5,
            'cost': 44
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'cost must be a multiple of 5')
    
    def test_adding_product_with_cost_negative_cost_returns_error(self):
        product_data = {
            'productName': 'Crystal Water',
            'amountAvailable': 5,
            'cost': -500
        }
        response = self.client.post('/product/add', json=product_data)
        self.assertEqual(response.get_json()['message'], 
                         'cost must be positive')
    
    def test_add_product_has_current_seller_id(self):
        response = self.client.post('/product/add', json=self.product_data)
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertEqual(product.sellerId, user.id)
    
    def test_added_product_shows_up_under_user_products_sold(self):
        response = self.client.post('/product/add', json=self.product_data)
        with self.app.app_context():
            product = Product.query.filter_by(productName=self.product_data['productName']).first()
            user = User.query.filter_by(username=self.post_data_seller['username']).first()
            self.assertTrue(product in user.products_sold)
    
    def test_view_product_details_given_valid_product_id(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.get('/product/1')
        expected_response = {
            'productName': 'Water',
            'amountAvailable': 10,
            'cost': 100,
            'sellerId': 1
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_view_product_details_given_invalid_product_id_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.get('/product/2')
        self.assertEqual(response.get_json()['message'],
                         'invalid product id. Please check and try again.')
    
    def test_update_product_details_from_valid_seller(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Coca Cola 0.5L',
            'amountAvailable': 12,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'product details updated')
        with self.app.app_context():
            product = Product.query.get(1)
            self.assertEqual(product.productName, updated_product_data['productName'])
            self.assertEqual(product.amountAvailable, updated_product_data['amountAvailable'])
            self.assertEqual(product.cost, updated_product_data['cost'])
    
    def test_update_product_details_should_contain_productName_less_than_32_characters(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'this product name is longer than 32 characters. Much much longer',
            'amountAvailable': 20,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'productName must be shorter than 32 characters')
    
    def test_update_product_details_with_productName_None_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': None,
            'amountAvailable': 20,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'productName cannot be None')
    
    def test_update_product_details_with_amountAvailable_greater_than_15_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Water',
            'amountAvailable': 33,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'amountAvailable must be lesser than or equal to 15')
    
    def test_update_product_details_with_negative_amountAvailable_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Water',
            'amountAvailable': -33,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'amountAvailable must be positive')
    
    def test_update_product_details_with_None_amountAvailable_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Water',
            'amountAvailable': None,
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'amountAvailable must not be None')
    
    def test_update_product_details_with_non_int_amountAvailable_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product_data)
        updated_product_data = {
            'productName': 'Water',
            'amountAvailable': 'Fifty Thousand',
            'cost': 200
        }
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'amountAvailable must be of type int')
    
    def test_update_product_details_as_different_seller_from_product_returns_error_message(self):
        seller1_data = {
            'username': 'seller1',
            'password': 'password1',
            'role': 'seller'
        }
        seller1_login_data = {
            'username': 'seller1',
            'password': 'password1'
        }
        seller2_data = {
            'username': 'seller2',
            'password': 'password2',
            'role': 'seller'
        }
        seller2_login_data = {
            'username': 'seller2',
            'password': 'password2'
        }
        product_data = {
            'productName': 'product1',
            'amountAvailable': 8,
            'cost': 75
        }
        updated_product_data = {
            'productName': 'updated_product1',
            'amountAvailable': 8,
            'cost': 75
        }
        _ = self.client.post('/user/register', json=seller1_data)
        _ = self.client.post('/user/login', json=seller1_login_data)
        _ = self.client.post('/product/add', json=product_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=seller2_data)
        _ = self.client.post('/user/login', json=seller2_login_data)
        response = self.client.put('/product/1/update', json=updated_product_data)
        self.assertEqual(response.get_json()['message'],
                         'seller id of current user does not match seller id of product')
    
    def test_delete_request_as_different_seller_from_product_returns_error_message(self):
        seller1_data = {
            'username': 'seller1',
            'password': 'password1',
            'role': 'seller'
        }
        seller1_login_data = {
            'username': 'seller1',
            'password': 'password1'
        }
        seller2_data = {
            'username': 'seller2',
            'password': 'password2',
            'role': 'seller'
        }
        seller2_login_data = {
            'username': 'seller2',
            'password': 'password2'
        }
        product_data = {
            'productName': 'product1',
            'amountAvailable': 8,
            'cost': 75
        }
        _ = self.client.post('/user/register', json=seller1_data)
        _ = self.client.post('/user/login', json=seller1_login_data)
        _ = self.client.post('/product/add', json=product_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=seller2_data)
        _ = self.client.post('/user/login', json=seller2_login_data)
        response = self.client.delete('/product/1/delete')
        self.assertEqual(response.get_json()['message'],
                         'seller id of current user does not match seller id of product')
    
    def test_delete_request_from_valid_seller(self):
        _ = self.client.post('/product/add', json=self.product_data)
        response = self.client.delete('/product/1/delete')
        self.assertEqual(response.get_json()['message'],
                         'product deleted')
        with self.app.app_context():
            product = Product.query.get(1)
            self.assertIsNone(product)

class TestProductPurchase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        
        self.db = db
        
        self.client = self.app.test_client()
        
        self.post_data_seller = {
            'username': 'seller1',
            'password': 'randomGibberish777',
            'role': 'seller'
        }
        
        self.post_data_seller_login = {
            'username': 'seller1',
            'password': 'randomGibberish777',
        }
        
        self.post_data_buyer = {
            'username': 'buyer1',
            'password': 'mtOl56&kkk',
            'role': 'buyer'
        }
        
        self.post_data_buyer_login = {
            'username': 'buyer1',
            'password': 'mtOl56&kkk',
        }
        
        self.product1_data = {
            'productName': 'product1',
            'amountAvailable': 10,
            'cost': 75
        }
        
        _ = self.client.post('/user/register', json=self.post_data_seller)
        _ = self.client.post('/user/login', json=self.post_data_seller_login)
    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_product_purchase_single_quantity_returns_correct_change(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 0,
            'c50': 2,
            'c100': 0
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 1,
        }
        response = self.client.post('/product/buy', json=buy_data)
        expected_response = {
            'productPurchased': self.product1_data['productName'],
            'amountSpent': 75,
            'change': {
                'c5': 1,
                'c10': 0,
                'c20': 1,
                'c50': 0,
                'c100': 0
            }
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_product_purchase_multiple_quantity_computes_correct_cost(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 5,
            'c50': 2,
            'c100': 1
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 4,
        }
        response = self.client.post('/product/buy', json=buy_data)
        expected_response = {
            'productPurchased': self.product1_data['productName'],
            'amountSpent': 300,
            'change': {
                'c5': 0,
                'c10': 0,
                'c20': 0,
                'c50': 0,
                'c100': 0
            }
        }
        self.assertEqual(response.get_json(), expected_response)
    
    def test_product_purchase_multiple_quantity_reduces_quantity_in_db(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 5,
            'c50': 2,
            'c100': 1
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 4,
        }
        response = self.client.post('/product/buy', json=buy_data)
        expected_response = {
            'productPurchased': self.product1_data['productName'],
            'amountSpent': 300,
            'change': {
                'c5': 0,
                'c10': 0,
                'c20': 0,
                'c50': 0,
                'c100': 0
            }
        }
        self.assertEqual(response.get_json(), expected_response)
        with self.app.app_context():
            product = Product.query.get(1)
            self.assertEqual(product.amountAvailable, self.product1_data['amountAvailable'] - buy_data['amountToBuy'])
    
    def test_product_purchase_with_invalid_product_id_produces_error_message(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 5,
            'c50': 2,
            'c100': 1
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 5,
            'amountToBuy': 4,
        }
        response = self.client.post('/product/buy', json=buy_data)
        self.assertEqual(response.get_json()['message'],
                         'product id is invalid')
    
    def test_product_purchase_with_insifficient_product_quantity_available_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 5,
            'c50': 2,
            'c100': 1
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 12,
        }
        response = self.client.post('/product/buy', json=buy_data)
        self.assertEqual(response.get_json()['message'],
                         'quantity requested to buy more than amount available')
    
    def test_product_purchase_with_insufficient_deposit_returns_error_message(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 3,
            'c50': 0,
            'c100': 0
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 1,
        }
        response = self.client.post('/product/buy', json=buy_data)
        self.assertEqual(response.get_json()['message'],
                         'insufficient or no deposit. Please deposit sufficient money and try again')
    
    def test_product_purchase_when_insufficient_change_in_vending_machine(self):
        with self.app.app_context():
            coinstack = Coinstack.query.get(1)
            coinstack.c5 = 0
            db.session.commit()
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 0,
            'c20': 8,
            'c50': 0,
            'c100': 0
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 1,
        }
        response = self.client.post('/product/buy', json=buy_data)
        self.assertEqual(response.get_json()['message'],
                         'vending machine has insufficient change. Please contact customer service')
    
    def test_product_purchase_resets_user_deposit_after_purchase(self):
        _ = self.client.post('/product/add', json=self.product1_data)
        _ = self.client.get('/user/logout')
        _ = self.client.post('/user/register', json=self.post_data_buyer)
        _ = self.client.post('/user/login', json=self.post_data_buyer_login)
        deposit_data = {
            'c5': 0,
            'c10': 2,
            'c20': 4,
            'c50': 0,
            'c100': 0
        }
        _ = self.client.post('/user/deposit', json=deposit_data)
        buy_data = {
            'productId': 1,
            'amountToBuy': 1,
        }
        _ = self.client.post('/product/buy', json=buy_data)
        response = self.client.get('/user/account')
        self.assertEqual(response.get_json()['deposit'], 0)

if __name__ == '__main__':
    unittest.main()
