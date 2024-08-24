import unittest
import os
from easy_bot.easy_bot import EasyBot

def sum(a: int, b: int) -> int:
    """
        This function realize a sum operation
        @a: int This is the first parameter
        @b: int This is the second parameter
    """
    return a + b

class TestEasyBot(unittest.TestCase):
    def test_create_assistant(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.create_assistant()
        self.assertEqual(type(bot.create_text_completion('Hola')), str)

    def test_create_assistant_2(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.create_assistant()
        bot.add_function(sum)
        self.assertEqual(type(bot.create_text_completion('How many is 55 +  87 + 4')), str)

    def test_create_assistant_3(self):
        token:str = os.getenv('OPENAI_API_KEY')
        if token is None: return
        bot = EasyBot(token=token, instruction='You\'re a Math expert')
        bot.create_assistant()
        self.assertEqual(type(bot.create_text_completion('Hola')), str)

if __name__ == '__main__':
    unittest.main()