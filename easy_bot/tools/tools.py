import inspect
import re
from typing import Callable
from ..types.easy_bot_types import FunctionSchema, Parameters

__all__ = ['obtain_sig']

def obtain_sig(func: Callable) -> FunctionSchema:
    """
    Function returns a dictionary with the function's name, documentation, parameters, and required parameters.
    This used to set the functions in the EasyBot class.

    Args:
        func (Callable): The function to obtain the signature 

    Returns:
        FunctionSchema: A dictionary with the function's name, documentation, parameters, and required parameters.
    """
    types: dict = {
        int: 'number',
        float: 'number',
        str: 'string',
        bool: 'boolean'
    }

    if not callable(func):
        raise TypeError(f"The provided func for '{name}' is not callable")

    func_name: str = func.__name__
    func_doc: str | None = func.__doc__

    if func_doc is None: func_doc = ''
    
    sig = inspect.signature(func)
    parameters: list[Parameters] = []
    required: list[str] = []

    for name, param in sig.parameters.items():
        if param.annotation not in types:
            raise TypeError(f"Invalid type for parameter '{name}': {param.annotation.__name__}")

        description_reST_pattern: str = r':param ' + name + r':.+'
        reST_pattern = re.compile(description_reST_pattern)
        finds: list[str] = reST_pattern.findall(func_doc)
        if len(finds) == 0:
            description_google_pattern: str = name + r' \(' + param.annotation.__name__ + r'\):.+'
            google_pattern = re.compile(description_google_pattern)
            finds = google_pattern.findall(func_doc)
            if len(finds) == 0: finds[0] = func_doc
            
        description: str = finds[0]
        param_info: Parameters = Parameters(name, types[param.annotation], description)
        parameters.append(param_info)

        if param.default is inspect.Parameter.empty:
            required.append(name)

    func_info: FunctionSchema = {
        "func_name": func_name,
        "func_doc": func_doc,
        "parameters": parameters,
        "required": required
    }

    return func_info