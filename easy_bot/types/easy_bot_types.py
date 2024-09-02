from typing import TypedDict, NamedTuple

__all__ = ["FunctionSchema"]

class Parameters(NamedTuple):
    name: str
    type: str
    description: str

class FunctionSchema(TypedDict):
    func_name: str
    func_doc: str
    parameters: list[Parameters]
    required: list[str]
