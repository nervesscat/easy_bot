# EasyBot Library

EasyBot is a Python library designed to facilitate the creation of AI-powered bots using OpenAI's API. This library provides a simple interface to integrate various functionalities and create a customizable assistant.

## Features

- Easy integration with OpenAI's API.
- Customizable bot functions.
- Simple setup and usage.

## Installation

To install the EasyBot library, you can use pip:

```bash
pip install easybot-py
```

## Usage

Usage
Here is an example of how to use the EasyBot library:

```python
import os
from easy_bot import EasyBot

def sum(a: int, b: int, positive: bool = False):
    """
    Made an operation and returns the result
    @a : int First operand
    @b : int Second operand
    """
    return a + b

def main():
    INSTRUCTION = "You're a Math tutor, you should use the functions"
    token = os.getenv('OPENAI_API_KEY')
    if token is None:
        raise ValueError('Token key is not set in env variables')

    client = EasyBot(token, INSTRUCTION)
    client.add_function(sum)
    client.create_assistant()

    response = client.create_text_completion('What is 24556 + 554322 + 2')
    print(response)

if __name__ == "__main__":
    main()
```

Here you're using the default model of EasyBot, it's using the OpenAI endpoint to generate the response. It's using by default the `gpt-4o-mini` model. You can change the model by passing the model name in the `create_assistant` method.

```python
import os
from easy_bot import EasyBot, OpenAICore

# Your functions here
# ...

def main():
    INSTRUCTION = "You're a Math tutor, you should use the functions"
    token = os.getenv('OPENAI_API_KEY')
    if token is None:
        raise ValueError('Token key is not set in env variables')

    client = EasyBot(token, INSTRUCTION)
    client.add_function(sum)
    client.create_assistant(OpenAICore, model='gpt-4o')

    response = client.create_text_completion('What is 24556 + 554322 + 2')
    print(response)

if __name__ == "__main__":
    main()
```

You can pass an image to the bot, and it will generate a response based on the image. You can use the `create_image_completion` method to generate a response based on the image. You could use either a local image (encoded) or a URL to the image.

```python
# URL
response = client.create_image_completion('url_to_image')

# Local image
with open('image.jpg', 'rb') as f:
    image = f.read()

response = client.create_image_completion(image)
```

## Documentation

### Using NIM endpoints (Beta)

To use the NIM endpoints, you need to pass the `Nim` class in the `create_assistant` method. For use NIM endpoints, you need to have a NIM API key. You can get it by signing up on the NIM website, [NVIDIA NIM](https://build.nvidia.com/nim).
By default we're using `mistral-large-2-instruct` model, but you can change it by passing the model name in the `create_assistant` method. For example, you can use the `meta/llama-3.1-70b-instruct` model.

It also support function calling, you can use the functions in the same way as the OpenAI endpoints.

```python
import os
from easy_bot import EasyBot, Nim

def main():
    INSTRUCTION = "You're a Math tutor, you should use the functions"
    token = os.getenv('NIM_API_KEY')
    if token is None:
        raise ValueError('Token key is not set in env variables')

    client = EasyBot(token, INSTRUCTION)
    client.add_function(sum)
    client.create_assistant(Nim, model='meta/llama-3.1-70b-instruct')

    response = client.create_text_completion('What is 24556 + 554322 + 2')
    print(response)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
