from .tools.tools import obtain_sig
from .endpoints.ai_cores import AICore
from .endpoints.openaicore import OpenAICore
from typing import Type, Callable
from .types.easy_bot_types import FunctionSchema
from .errors.easy_bot import AssistantNotCreated

class EasyBot:
    __token: str
    __instruction: str
    __ai_core: AICore | None
    __functions_info: list[FunctionSchema]
    funcs: dict[str, Callable]
    __default_core_class: Type[AICore] = OpenAICore

    def __init__(self, token: str, instruction: str):
        """Constructor of the EasyBot class
        This initializes the EasyBot class with the token and instruction to create the AI core.
        The EasyBot class is used to create an assistant, and provide the functions to the assistant.

        Args:
            token (str): The token of the AI provider
            instruction (str): The instruction that the AI will use to generate the responses"""
        EasyBot.funcs = {}
        self.__token = token
        self.__instruction = instruction
        self.__functions_info = []
        self.__ai_core = None

    def create_assistant(self, ai_core_class: Type[AICore] = __default_core_class, *args, **kwargs) -> None:
        """Create an assistant with the AI core class provided, by default is OpenAICore.

        Args:
            ai_core_class (Type[AICore], optional): The AI core class to create the assistant. Defaults to __default_core_class.
        """        
        self.__ai_core = ai_core_class(instruction=self.__instruction, tools=self.__functions_info, token=kwargs.get('token', self.__token), *args, **kwargs)
        self.__default_core_class = ai_core_class
    
    def set_assistant(self, ai_core: AICore) -> None:
        """Set the assistant with the AI core provided.

        Args:
            ai_core (AICore): The AI core to set the assistant.
        """        
        self.__ai_core = ai_core
        self.__ai_core.set_all_functions(self.funcs)
        self.__default_core_class = ai_core.__class__

    def add_function(self, func: Callable) -> None:
        """Add a function to the EasyBot class. This function will be used by the assistant.

        Args:
            func (Callable): The function to add to the EasyBot class.
        """        
        func_info: FunctionSchema = obtain_sig(func)
        self.__functions_info.append(func_info)
        EasyBot.funcs[func_info["func_name"]] = func
        if self.__ai_core is not None:
            self.__ai_core.create_bot(tools=self.__functions_info)

    def create_text_completion(self, task: str) -> str:
        """Create a text completion using the AI

        Args:
            task (str): The task to generate the completion

        Raises:
            AssistantNotCreated: If the AI core isn't initialized

        Returns:
            str: The completion of the task
        """
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_text_completion(task)
    
    def create_image_completion(self, task: str, encoded_img: bytes) -> str:
        """Create an image completion using the AI

        Args:
            task (str): The task to generate the completion
            encoded_img (bytes): The image encoded in bytes

        Raises:
            AssistantNotCreated: If the AI core isn't initialized

        Returns:
            str: The completion of the task
        """        
        if self.__ai_core is None:
            raise AssistantNotCreated("AI core isn't initialized")
        return self.__ai_core.create_image_completion(task, encoded_img)

    