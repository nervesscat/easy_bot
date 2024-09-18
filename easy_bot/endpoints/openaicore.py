import json
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from typing import Iterable, Union, Optional, Literal
from openai.types.beta.threads.message_content_part_param import MessageContentPartParam
from openai.types.beta.threads import Text, Run
from openai.types.beta.thread import Thread
from openai.types.beta.assistant import Assistant
from openai.types.beta import AssistantStreamEvent

from .ai_cores import AICore
from ..types.easy_bot_types import FunctionSchema

class OpenAICore(AICore):
    __tools: list
    __DEFAULT_INSTRUCTION = "You're a helpful assistant"

    def __init__(self, **kwargs) -> None:
      """Subclass of AICore to create an assistant with OpenAI API

      Args:
          instruction (str, optional): The instruction that the AI will use to generate the responses. Defaults to __DEFAULT_INSTRUCTION.
          tools (Optional[list[FunctionSchema]], optional): The tools to use in the assistant. Defaults to None.
      """      
      self.__client: OpenAI = OpenAI(api_key=kwargs.get('token', None))
      self.create_bot(**kwargs)
      self.__thread: Thread = self.__client.beta.threads.create()

    def create_bot(self, **kwargs):
      tools: list[FunctionSchema] | None = kwargs.get("tools", None)
      if tools is not None:
        self.set_all_functions(tools)

      self.__assistant: Assistant = self.__client.beta.assistants.create(
        instructions=kwargs.get("instruction", self.__DEFAULT_INSTRUCTION),
        tools=self.__tools,
        model=kwargs.get("model", "gpt-4o-mini"),
      )

    def create_image_completion(self, task: str, img: Union[bytes, str], detail: Literal['low', 'high'] = 'low') -> str:
      if type(img) == bytes:
          file = self.__client.files.create(file=img, purpose="vision")
          image_part = {
              "type": "image_file",
              "image_file": {
                  "file_id": file.id,
                  "detail": detail,
              },
          }
      else:
          image_part = {
              "type": "image_url",
              "image_url": {
                  "url": img,
                  "detail": detail,
              },
          }

      content: Iterable[MessageContentPartParam] = [
          {
              "type": "text",
              "text": task,
          },
          image_part
      ]

      return self.__create_completion(content)
    
    def create_text_completion(self, task: str) -> str:
      return self.__create_completion(task)

    def __create_completion(self, content: Union[str, Iterable[MessageContentPartParam]], role: Literal['user', 'assistant'] = 'user') -> str:
      self.__client.beta.threads.messages.create(
        thread_id=self.__thread.id,
        role=role,
        content=content
      )
    
      event_handler = EventHandler(self.__client)

      with self.__client.beta.threads.runs.stream(
        thread_id=self.__thread.id,
        assistant_id=self.__assistant.id,
        event_handler=event_handler,
      ) as stream: stream.until_done()

      return event_handler.snapshot.value
    
    def set_all_functions(self, funcs: list[FunctionSchema]):
      """Set all the functions to use in the assistant.

      Args:
          funcs (list[FunctionSchema]): The functions to set in the assistant
      """
      self.__tools = []
      for func in funcs:
        self.__tools.append(self.set_function_calling_schema(func))
    
    def set_function_calling_schema(self, func: FunctionSchema) -> dict:
      """Set the function calling schema to use in the assistant, this schema is the provided by the OpenAI documentation.

      Args:
          func (FunctionSchema): The function schema to set in the assistant
      """      
      return {
        "type": "function",
        "function": {
          "name": func["func_name"],
          "description": func["func_doc"],
          "strict": False,
          "parameters": {
            "type": "object",
            "properties": {
              name: {
                'type': param_type,
                'description': desc
              } for name, param_type, desc in func["parameters"]},
              "additionalProperties": False,
              "required": [name for name in func["required"]]
                }
            }
        }

class EventHandler(AssistantEventHandler):
  snapshot: Text
  __last_instance: Optional['EventHandler']

  def __init__(self, client: OpenAI, last_instance: Optional['EventHandler'] = None):
    super().__init__()
    self.__client = client
    self.snapshot = Text(annotations=[], value='')
    if last_instance is None:
      self.__last_instance = self
    else:
      self.__last_instance = last_instance
      
  @override
  def on_text_delta(self, delta, snapshot):
    self.snapshot = snapshot

  @override
  def on_event(self, event: AssistantStreamEvent) -> None:
    if event.event == 'thread.run.requires_action':
      self.handle_requires_action(event.data)

  def handle_requires_action(self, data: Run) -> None:
    from ..easy_bot import EasyBot
    tool_outputs: list = []

    for tool in data.required_action.submit_tool_outputs.tool_calls:
      name_func: str = tool.function.name
      arguments: str = tool.function.arguments

      args_dic: dict = json.loads(arguments)

      if name_func in EasyBot.funcs:
        func = EasyBot.funcs[name_func]
        output = func(**args_dic)
        tool_outputs.append({"tool_call_id": tool.id, "output": str(output)})

    result: str = self.submit_tool_outputs(tool_outputs)
    if len(result) == 0: return
    self.__last_instance.snapshot.value = result

  def submit_tool_outputs(self, tool_outputs: list) -> str:
      content = ''
      with self.__client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.current_run.thread_id,
        run_id=self.current_run.id,
        tool_outputs=tool_outputs,
        event_handler=EventHandler(self.__client, self.__last_instance)
      ) as stream:
        for text in stream.text_deltas:
          content += text
      return content