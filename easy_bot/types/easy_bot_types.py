from typing import TypedDict

__all__ = ["FunctionSchema"]

class FunctionSchema(TypedDict):
    func_name: str
    func_doc: str
    parameters: list[str]
    required: list[str]
