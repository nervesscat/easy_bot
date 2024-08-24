import inspect
from .ai_cores import AICore
from .openai_conn import OpenAICore
from typing import Optional, Type, Callable

class AssistantNotCreated(Exception):
    pass

class EasyBot:
    __token: str
    __instruction: str
    __ai_core: AICore | None
    # ! This should not be a tuple, instead a list of dict
    __functions_json: tuple
    funcs: dict[str, Callable]
    __default_core_class: Type[AICore] = OpenAICore

    def __init__(self, token: str, instruction: str):
        EasyBot.funcs = {}
        self.__token = token
        self.__instruction = instruction
        self.__functions_json = ()
        self.__ai_core = None

    def create_assistant(self, ai_core_class: Type[AICore] = __default_core_class, *args, **kwargs) -> None:
        self.__ai_core = ai_core_class(instruction=self.__instruction, tools=self.__functions_json, token=kwargs.get('token', self.__token), *args, **kwargs)
        self.__default_core_class = ai_core_class
    
    def set_assistant(self, ai_core: AICore) -> None:
        self.__ai_core = ai_core
        self.__ai_core.set_function_calling_schema(self.__functions_json[0], self.__functions_json[1], self.__functions_json[2], self.__functions_json[3])
        self.__default_core_class = ai_core.__class__

    def add_function(self, func: Callable) -> None:
        self.__functions_json = self.__obtain_sig(func)
        EasyBot.funcs[self.__functions_json[0]] = func
        if self.__ai_core is None: return
        self.__ai_core.set_function_calling_schema(self.__functions_json[0], self.__functions_json[1], self.__functions_json[2], self.__functions_json[3])
    
    def create_text_completion(self, task: str) -> str:
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_text_completion(task)
    
    def create_image_completion(self, task: str, encoded_img: bytes) -> str:
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_image_completion(task, encoded_img)

    def __obtain_sig(self, func: Callable) -> tuple[str, str, list, list]:
        types: dict = {
            int: 'number',
            str: 'string',
            bool: 'boolean'
        }

        if not callable(func):
            raise TypeError(f"The provided func for '{name}' is not callable")

        func_name: str = func.__name__
        func_doc: str | None = func.__doc__
        if func_doc is None: func_doc = ''
        
        sig = inspect.signature(func)
        parameters: list = []
        required: list = []

        for name, param in sig.parameters.items():
            if param.annotation not in {int, str, bool}:
                raise TypeError(f"Invalid type for parameter '{name}': {param.annotation.__name__}")

            parameters.append((name, types[param.annotation]))

            if param.default is inspect.Parameter.empty:
                required.append((name, types[param.annotation]))

        return func_name, func_doc, parameters, required