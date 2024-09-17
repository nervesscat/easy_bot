import unittest
import os
from easy_bot.easy_bot import EasyBot
from easy_bot.endpoints.nim import Nim

def sum(a: int, b: int) -> float:
    """
    This function realize a sum operation
    :param a: First operand
    :type a: float
    :param b: Second operand
    :type b: float
    :return: The sum of a and b
    :rtype: float
    """
    return a + b

def multiplication(a: float, b: float) -> float:
    """
    This function realize a multiplication operation
    :param a: This is the first parameter
    :type a: float
    :param b: This is the second parameter
    :type b: float
    :return: Return a times b
    """
    return a * b

def division(dividend: float, divisor: float) -> float:
    """
    This function realize a division operation
    Args:
        dividend (float): This is the first parameter
        divisor (float): This is the second parameter

    Returns:
        float: The quotient
    """
    return dividend / divisor

class TestEasyBot(unittest.TestCase):
    def test_create_assistant(self):
        token:str = os.getenv('NIM_API_KEY')
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('Hola')
        self.assertEqual(type(response), str)

    def test_create_assistant_sum(self):
        token:str = os.getenv('NIM_API_KEY')
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.create_assistant(Nim)
        response: int = bot.create_text_completion('How many is 88837559 +  87066842 + 48890909 + 17456895, don\'t use commas')
        self.assertTrue(response.__contains__('242252205'))

    def test_create_assistant_sum_2(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.create_assistant(Nim)
        bot.add_function(division)
        # response: int = bot.create_text_completion('How many is 88837559 +  87066842 + 48890909 + 17456895, don\'t use commas')
        response2: int = bot.create_text_completion('How many is ( 52367 / 6 ) / 5')
        self.assertTrue(response2.__contains__('1745.5'))

    def test_create_assistant_div_e(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532)')
        self.assertTrue(response.__contains__('16.'))

    def test_create_assistant_div_m(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532) / 4')
        self.assertTrue(response.__contains__('4.12'))

    def test_create_assistant_div_h(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532) / 4')
        self.assertTrue(response.__contains__('4.12'))

    def test_create_assistant_mult_e(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456')
        self.assertTrue(response.replace(',', '').__contains__('6207469684052029949608905544'))

    def test_create_assistant_mult_m(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456 * 24')
        self.assertTrue(response.replace(',', '').__contains__('148979272417248718790613733056'))

    def test_create_assistant_mult_h(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456 * 24 * 21')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('3128564720762223094602888394176'))

    def test_create_assistant_multi_m(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is ( 78787870001999 + 78787124006456 ) * 24')
        self.assertTrue(response.replace(',', '').__contains__('3781799856202920') or response.replace(',', '').__contains__('3.7'))

    def test_create_assistant_multi_h(self):
        token:str = os.getenv('NIM_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant(Nim)
        response: str = bot.create_text_completion('How many is ( ( 78787870001999 + 78787124006456 ) * 24 * 21 ) / 2')
        self.assertTrue(response.replace(',', '').__contains__('39708898490130660') or response.replace(',', '').__contains__('3.9'))

if __name__ == '__main__':
    unittest.main()