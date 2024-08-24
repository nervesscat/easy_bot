class AICore:
    def __init__(self, *args, **kwargs):
        pass

    def create_image_completion(self, task: str, encoded_img: bytes): 
        raise NotImplemented('create_image_completion method is not implemented in AICore class')

    def create_text_completion(self, task: str):
        raise NotImplemented('create_text_completion method is not implemented in AICore class')

    def set_function_calling_schema(self, name: str, func_doc: str, params: list[tuple[str, object]], required: list[tuple[str, object]]):
        raise NotImplemented('set_function_calling_schema method is not implemented in AICore class')