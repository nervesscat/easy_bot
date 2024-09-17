from typing import TypedDict, Optional, Literal
from .easy_bot_types import FunctionSchema

__all__ = ["nim_function_call_scheme", "Message"]

def nim_function_call_scheme(func: FunctionSchema) -> dict:
    return {
        "type": "function",
        "function": {
            "name": func["func_name"],
            "description": func["func_doc"],
            "parameters": {
                "type": "object",
                "properties": {
                    name: {
                        'type': param_type,
                        'description': desc
                    } for name, param_type, desc in func["parameters"]
                },
                "required": [name for name in func["required"]]
            }
        }
    }

class Message(TypedDict):
    role: Literal['user', 'assistant']
    content: str
