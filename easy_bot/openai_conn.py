import json
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from typing import Iterable, Union, Optional, Literal
from openai.types.beta.threads.message_content_part_param import MessageContentPartParam
from openai.types.beta.threads import Text
from openai.types.beta.thread import Thread
from openai.types.beta.assistant import Assistant

from .ai_cores import AICore

class OpenAICore(AICore):
    __tools: list
    __DEFAULT_INSTRUCTION = "You're a helpful assistant"

    def __init__(self, instruction: str = __DEFAULT_INSTRUCTION, tools: Optional[tuple] = (), **kwargs) -> None:
      self.__client: OpenAI = OpenAI(api_key=kwargs.get('token', None))
      self.__tools = []
      if tools is not None and tools.__len__() == 4:
        self.set_function_calling_schema(tools[0], tools[1], tools[2], tools[3])

      self.__assistant: Assistant = self.__client.beta.assistants.create(
        instructions=instruction,
        tools=self.__tools,
        model="gpt-4o-mini",
      )
      self.__thread: Thread = self.__client.beta.threads.create()

    def create_image_completion(self, task: str, encoded_img: bytes) -> str:
      file = self.__client.files.create(file=encoded_img, purpose="vision")
      content: Iterable[MessageContentPartParam] = [
        {
          "type": "text",
          "text": task,
        },
        {
          "type": "image_file",
          "image_file": {
            "file_id": file.id,
            "detail": "low",
          },
        }
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
    
      event_handler = EventHandler(self.__client, self.__thread)

      with self.__client.beta.threads.runs.stream(
        thread_id=self.__thread.id,
        assistant_id=self.__assistant.id,
        event_handler=event_handler,
      ) as stream: stream.until_done()

      return event_handler.snapshot.value
    
    def set_function_calling_schema(self, name: str, func_doc: str, params: list[tuple[str, object]], required: list[tuple[str, object]]) -> None:
      self.__tools.append({
        "type": "function",
        "function": {
          "name": name,
          "description": func_doc,
          "strict": False,
          "parameters": {
            "type": "object",
            "properties": {
              name: {
                'type': param_type,
                'description': func_doc
              } for name, param_type in params},
              "additionalProperties": False,
              "required": [name for name, _ in required]
                  }
            }
        })

class EventHandler(AssistantEventHandler):
  snapshot: Text
  run_id: str
  tool_outputs: list
  __last_instance: Optional['EventHandler']

  def __init__(self, client: OpenAI, thread: Thread, last_instance: Optional['EventHandler'] = None,  tool_outputs: Optional[list] = None):
    self.__client = client
    self.__thread = thread
    self.snapshot = Text(annotations=[], value='')
    if last_instance is None:
      self.__last_instance = self
    else:
      self.__last_instance = last_instance

    if tool_outputs is None: tool_outputs = []
    self.tool_outputs = tool_outputs
    super().__init__()

  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    self.snapshot = snapshot
      
  def on_tool_call_created(self, tool_call):
    # print(f"\nassistant > {tool_call.type}\n", flush=True)
    ...
  
  def on_tool_call_delta(self, delta, snapshot):
    ...

  @override
  def on_event(self, event):
    if event.event == 'thread.run.requires_action':
      self.run_id = event.data.id
      self.handle_requires_action(event.data, self.run_id)

  def handle_requires_action(self, data, run_id):
    from .easy_bot import EasyBot
    
    for tool in data.required_action.submit_tool_outputs.tool_calls:
      name_func: str = tool.function.name
      arguments: str = tool.function.arguments

      args_dic: dict = json.loads(arguments)

      if name_func in EasyBot.funcs:
        func = EasyBot.funcs[name_func]
        output = func(**args_dic)
        self.tool_outputs.append({"tool_call_id": tool.id, "output": str(output)})

        result = ''
        with self.__client.beta.threads.runs.submit_tool_outputs_stream(
          thread_id=self.__thread.id,
          run_id=run_id,
          tool_outputs=self.tool_outputs,
          event_handler=EventHandler(self.__client, self.__thread, self.__last_instance)
        ) as stream:
          for text in stream.text_deltas:
            result += text

        if len(result) <= 0:
          return

        if self.__last_instance is None: return
        self.__last_instance.snapshot.value = result