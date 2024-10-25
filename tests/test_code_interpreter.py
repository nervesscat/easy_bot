import unittest
import os
from easy_bot.utils.code_interpreter import execute_python_script
from easy_bot import EasyBot

class TestCodeInterpreter(unittest.TestCase):
    def test_code_interpreter_e(self):
        code = """print('Hola', end='')"""
        output: str = execute_python_script(code)
        self.assertEqual(output, 'Hola')

    def test_code_interpreter_time(self):
        code = """print('Hola', end='') 
import time
time.sleep(4)
print('Hola', end='')
        """
        output: str = execute_python_script(code)
        print(output)
        self.assertEqual(output, 'HolaHola')

    def test_code_interpreter_time_2(self):
        code = """print('Hola', end='') 
import time
time.sleep(11)
print('Hola', end='')
        """
        output: str = execute_python_script(code, 2)
        self.assertEqual(output, 'Execution timed out')

    def test_code_interpreter_time_while(self):
        code = """while True:
    print('Hola')
        """
        output: str = execute_python_script(code, 1)
        self.assertTrue(output.__contains__('Execution timed out'))
    
    def test_code_assistant(self):
        client = EasyBot(token=os.getenv("OPEN_AI_API_KEY"), instruction="Use your functions")
        client.add_function(execute_python_script)
        client.create_assistant()
        response: str = client.create_text_completion('What\'s the answer of 2 ^ 1000, don\'t use , in your answer')
        self.assertTrue(response.__contains__('10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069376'))