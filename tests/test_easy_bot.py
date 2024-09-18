import unittest
import os
from easy_bot import EasyBot, OpenAICore

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
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.create_assistant()
        response: str = bot.create_text_completion('Hola')
        print(response)
        self.assertEqual(type(response), str)

    def test_create_assistant_sum(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.create_assistant()
        response: int = bot.create_text_completion('How many is 88837559 +  87066842 + 48890909 + 17456895, don\'t use commas')
        print(response)
        self.assertTrue(response.__contains__('242252205'))

    def test_create_assistant_sum_2(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.create_assistant()
        bot.add_function(division)
        response: int = bot.create_text_completion('How many is 88837559 +  87066842 + 48890909 + 17456895, don\'t use commas')
        print(response)
        response2: int = bot.create_text_completion('How many is ( 52367 / 6 ) / 5')
        print(response2)
        self.assertTrue(response2.__contains__('1745.5'))

    def test_create_assistant_div_e(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.create_assistant()
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532)')
        self.assertTrue(response.__contains__('16.'))

    def test_create_assistant_div_m(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.create_assistant()
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532) / 4')
        print(response)
        self.assertTrue(response.__contains__('4.12'))

    def test_create_assistant_div_h(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant()
        response: str = bot.create_text_completion('How many is (9724712985643634 / 589830240253532) / 4')
        print(response)
        self.assertTrue(response.__contains__('4.12'))

    def test_create_assistant_mult_e(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)

        bot.create_assistant()
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('6207469684052029949608905544'))

    def test_create_assistant_mult_m(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(multiplication)

        bot.create_assistant()
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456 * 24 * 21')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('3128564720762223094602888394176'))

    def test_create_assistant_mult_h(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(division)
        bot.add_function(multiplication)

        bot.create_assistant()
        response: str = bot.create_text_completion('How many is 78787870001999 * 78787124006456 * 24 * 21')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('3128564720762223094602888394176'))

    def test_create_assistant_multi_m(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.add_function(multiplication)

        bot.create_assistant()
        response: str = bot.create_text_completion('How many is ( 78787870001999 + 78787124006456 ) * 24')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('3781799856202920') or response.replace(',', '').__contains__('3.7'))

    def test_create_assistant_multi_h(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.add_function(sum)
        bot.add_function(division)
        bot.add_function(multiplication)

        bot.create_assistant()
        response: str = bot.create_text_completion('How many is ( ( 78787870001999 + 78787124006456 ) * 24 * 21 ) / 2')
        print(response)
        self.assertTrue(response.replace(',', '').__contains__('39708898490130660') or response.replace(',', '').__contains__('3.9'))

    def test_image(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a helpful assistant')
        bot.add_function(sum)
        bot.add_function(division)
        bot.add_function(multiplication)
        bot.create_assistant(OpenAICore, model='gpt-4o-mini')
        url: str = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SGI-2016-South_Georgia_(Fortuna_Bay)%E2%80%93King_penguin_(Aptenodytes_patagonicus)_04.jpg/1200px-SGI-2016-South_Georgia_(Fortuna_Bay)%E2%80%93King_penguin_(Aptenodytes_patagonicus)_04.jpg'
        response: str = bot.create_image_completion('What\'s this?', url, 'high')
        print(response)
        self.assertTrue(response.lower().__contains__('penguin'))

if __name__ == '__main__':
    unittest.main()