from ..types.easy_bot_types import FunctionSchema

class AICore:
    def __init__(self, *args, **kwargs):
        pass

    def create_image_completion(self, task: str, encoded_img: bytes): 
        raise NotImplemented('create_image_completion method is not implemented in AICore class')

    def create_text_completion(self, task: str):
        raise NotImplemented('create_text_completion method is not implemented in AICore class')

    def set_function_calling_schema(self, funcs: list[FunctionSchema]):
        raise NotImplemented('set_function_calling_schema method is not implemented in AICore class')

    def set_all_functions(self, func: FunctionSchema):
        raise NotImplemented('set_function_calling_schema method is not implemented in AICore class')
    
    def create_bot(self):
        raise NotImplemented('create_bot method is not implemented in AICore class')