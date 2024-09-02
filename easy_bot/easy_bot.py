from .tools.tools import obtain_sig
from .ai_cores import AICore
from .openai_conn import OpenAICore
from typing import Type, Callable
from .types.easy_bot_types import FunctionSchema

class AssistantNotCreated(Exception):
    pass

class EasyBot:
    __token: str
    __instruction: str
    __ai_core: AICore | None
    __functions_info: list[FunctionSchema]
    funcs: dict[str, Callable]
    __default_core_class: Type[AICore] = OpenAICore

    def __init__(self, token: str, instruction: str):
        EasyBot.funcs = {}
        self.__token = token
        self.__instruction = instruction
        self.__functions_info = []
        self.__ai_core = None

    def create_assistant(self, ai_core_class: Type[AICore] = __default_core_class, *args, **kwargs) -> None:
        self.__ai_core = ai_core_class(instruction=self.__instruction, tools=self.__functions_info, token=kwargs.get('token', self.__token), *args, **kwargs)
        self.__default_core_class = ai_core_class
    
    def set_assistant(self, ai_core: AICore) -> None:
        self.__ai_core = ai_core
        self.__ai_core.set_all_functions(self.funcs)
        self.__default_core_class = ai_core.__class__

    def add_function(self, func: Callable) -> None:
        func_info: FunctionSchema = obtain_sig(func)
        self.__functions_info.append(func_info)
        EasyBot.funcs[func_info["func_name"]] = func
        self.create_assistant()

    def create_text_completion(self, task: str) -> str:
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_text_completion(task)
    
    def create_image_completion(self, task: str, encoded_img: bytes) -> str:
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_image_completion(task, encoded_img)

    