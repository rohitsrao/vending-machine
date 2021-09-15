import unittest

from vending_machine.helper_functions import coin_change_calculator

class TestCoinChangeCalculator(unittest.TestCase):
     
    def test_0_returned_as_all_zeros(self):
        num_coins_available = {'c5': 5, 'c10': 6, 'c20': 6, 'c50': 2, 'c100': 1} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 0} 
        self.assertEqual(coin_change_calculator(0, num_coins_available), expected_change)
     
    def test_returns_75_as_1x50_1x20_1x5_given_40coins_in_each(self):
        num_coins_available = {'c5': 40, 'c10': 40, 'c20': 40, 'c50': 40, 'c100': 40} 
        expected_change = {'c5': 1, 'c10': 0, 'c20': 1, 'c50': 0, 'c100': 0} 
        self.assertEqual(coin_change_calculator(25, num_coins_available), expected_change)
     
    def test_385_returned_as_1x100_2x50_6x20_6x10_1x5_given_1x100_2x50_6x20_6x10_5x5_available(self):
        num_coins_available = {'c5': 5, 'c10': 6, 'c20': 6, 'c50': 2, 'c100': 1} 
        expected_change = {'c5': 1, 'c10': 6, 'c20': 6, 'c50': 2, 'c100': 1} 
        self.assertEqual(coin_change_calculator(385, num_coins_available), expected_change)
     
    def test_125_returns_none_given_insufficient_coins(self):
        num_coins_available = {'c5': 0, 'c10': 1, 'c20': 0, 'c50': 2, 'c100': 0} 
        expected_change = None
        self.assertEqual(coin_change_calculator(125, num_coins_available), expected_change)
     
    def test_385_returned_as_1x100_2x50_6x20_6x10_1x5_given_1x100_2x50_6x20_6x10_5x5_available(self):
        num_coins_available = {'c5': 5, 'c10': 6, 'c20': 6, 'c50': 2, 'c100': 1} 
        expected_change = {'c5': 1, 'c10': 6, 'c20': 6, 'c50': 2, 'c100': 1} 
        self.assertEqual(coin_change_calculator(385, num_coins_available), expected_change)
     
    def test_100_returned_as_1x50_1x20_3x10_given_1x50_1x20_5x10_available(self):
        num_coins_available = {'c5': 0, 'c10': 5, 'c20': 1, 'c50': 1, 'c100': 0} 
        expected_change = {'c5': 0, 'c10': 3, 'c20': 1, 'c50': 1, 'c100': 0} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)
     
    def test_100_returned_as_1x50_2x20_1x10_given_1x50_3x20_5x10_available(self):
        num_coins_available = {'c5': 0, 'c10': 5, 'c20': 3, 'c50': 1, 'c100': 0} 
        expected_change = {'c5': 0, 'c10': 1, 'c20': 2, 'c50': 1, 'c100': 0} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)
     
    def test_100_returned_as_5x20_given_1x50_10x20_available(self):
        num_coins_available = {'c5': 0, 'c10': 0, 'c20': 10, 'c50': 1, 'c100': 0} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 5, 'c50': 0, 'c100': 0} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)
     
    def test_100_returned_as_5x20_given_sufficient_coins_available(self):
        num_coins_available = {'c5': 0, 'c10': 0, 'c20': 6, 'c50': 0, 'c100': 0} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 5, 'c50': 0, 'c100': 0} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)
     
    def test_100_returned_as_2x50_given_sufficient_coins_available(self):
        num_coins_available = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 2, 'c100': 0} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 2, 'c100': 0} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)
        
    def test_200_returned_as_2x100_given_sufficient_coins_available(self):
        num_coins_available = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 2} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 2} 
        self.assertEqual(coin_change_calculator(200, num_coins_available), expected_change)
        
    def test_100_returned_as_1x100_given_sufficient_coins_available(self):
        num_coins_available = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 1} 
        expected_change = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 1} 
        self.assertEqual(coin_change_calculator(100, num_coins_available), expected_change)

if __name__ == '__main__':
    unittest.__main__()
