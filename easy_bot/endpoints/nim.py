import json
from openai import OpenAI

from .ai_cores import AICore 
from ..types.nim_types import *
from ..types.easy_bot_types import FunctionSchema

class Nim(AICore):
    __model: str
    __tools: list[dict] = []
    __messages: list[Message]
    __BASE_URL: str = "https://integrate.api.nvidia.com/v1"

    def __init__(self, **kwargs):
        self.__messages = []
        self.__client: OpenAI = OpenAI(
            base_url = self.__BASE_URL,
            api_key = kwargs.get("token", None)
        )
        self.__model = kwargs.get('model', 'mistralai/mistral-large-2-instruct')
        self.create_bot(**kwargs)

    def create_bot(self, **kwargs):
        tools: list[FunctionSchema] | None = kwargs.get("tools", None)
        if tools is not None:
            self.set_all_functions(tools)

    def set_all_functions(self, funcs: list[FunctionSchema]):
        self.__tools = []
        for tool in funcs:
            self.__tools.append(nim_function_call_scheme(tool))

    def create_text_completion(self, task: str, role: str = 'user') -> str:
        self.insert_message(task, role)
        completion_args = {
            "model": self.__model,
            "messages": self.__messages,
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
        }

        if self.__tools:
            completion_args["tools"] = self.__tools
            completion_args["tool_choice"] = "auto"

        completion = self.__client.chat.completions.create(**completion_args)

        content: str = completion.choices[0].message.content
        if completion.choices[0].finish_reason == 'tool_calls':
            from ..easy_bot import EasyBot
            for func in completion.choices[0].message.tool_calls:
                name: str = func.function.name
                args: dict = json.loads(func.function.arguments)
                func = EasyBot.funcs[name]
                result = func(**args)
                log_message: str = '(Function Name: ' + str(name) + '\nParameters: ' + str(args) + '\nOutput:' + str(result) + ')'
                self.insert_message(log_message, 'assistant')
            content = self.create_text_completion('Function Calling Waiting...', 'assistant')

        self.insert_message(content, 'assistant')
        return content

    def insert_message(self, task: str, role: str):
        self.__messages.append({"role": role, "content": task})