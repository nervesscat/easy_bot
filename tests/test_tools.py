import unittest
from easy_bot.tools.tools import obtain_sig
from easy_bot.types.easy_bot_types import FunctionSchema, Parameters

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

def subtraction(a: float, b: float) -> float:
    """
    This function realizes a subtraction operation.
    :param a: This is the first parameter
    :type a: float
    :param b: This is the second parameter
    :type b: float
    :return: Return a minus b
    :rtype: float
    """
    return a - b

class TestTools(unittest.TestCase):
    def test_params_reST(self):
        func_info: FunctionSchema = obtain_sig(sum)
        real_func_info: FunctionSchema = {
        "func_name": "sum",
        "func_doc": """
    This function realize a sum operation
    :param a: First operand
    :type a: float
    :param b: Second operand
    :type b: float
    :return: The sum of a and b
    :rtype: float
    """,
        "parameters": [
            Parameters('a', 'number', ':param a: First operand'),
            Parameters('b', 'number', ':param b: Second operand')
        ],
        "required": ['a', 'b']
        }
        self.assertEqual(func_info, real_func_info)
    
    def test_params_google(self):
        func_info: FunctionSchema = obtain_sig(division)
        real_func_info: FunctionSchema = {
        "func_name": "division",
        "func_doc": """
    This function realize a division operation
    Args:
        dividend (float): This is the first parameter
        divisor (float): This is the second parameter

    Returns:
        float: The quotient
    """,
        "parameters": [
            Parameters('dividend', 'number', 'dividend (float): This is the first parameter'),
            Parameters('divisor', 'number', 'divisor (float): This is the second parameter')
        ],
        "required": ['dividend', 'divisor']
        }
        self.assertEqual(func_info, real_func_info)

    def test_params_mult(self):
        func_info: FunctionSchema = obtain_sig(multiplication)
        real_func_info: FunctionSchema = {
        "func_name": "multiplication",
        "func_doc": """
    This function realize a multiplication operation
    :param a: This is the first parameter
    :type a: float
    :param b: This is the second parameter
    :type b: float
    :return: Return a times b
    """,
        "parameters": [
            Parameters('a', 'number', ':param a: This is the first parameter'),
            Parameters('b', 'number', ':param b: This is the second parameter')
        ],
        "required": ['a', 'b']
        }
        self.assertEqual(func_info, real_func_info)

    def test_params_subtraction(self):
        func_info: FunctionSchema = obtain_sig(subtraction)
        real_func_info: FunctionSchema = {
        "func_name": "subtraction",
        "func_doc": """
    This function realizes a subtraction operation.
    :param a: This is the first parameter
    :type a: float
    :param b: This is the second parameter
    :type b: float
    :return: Return a minus b
    :rtype: float
    """,
        "parameters": [
            Parameters('a', 'number', ':param a: This is the first parameter'),
            Parameters('b', 'number', ':param b: This is the second parameter')
        ],
        "required": ['a', 'b']
        }
        self.assertEqual(func_info, real_func_info)

if __name__ == '__main__':
    unittest.main()