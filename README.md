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
from openai_conn import OpenAICore
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

    print(client.create_text_completion('Who are you?'))
    print(client.create_text_completion('What is 24556 + 554322 + 2'))

if __name__ == "__main__":
    main()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
