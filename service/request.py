import json
import openai
import sys
import markdown
from bs4 import BeautifulSoup
import html
import re
import os

config_file = os.getenv('HOME')+'/.config/chatgpt-py/config.json'


def init(config_file):
    if not os.path.exists(config_file):
        api_type = input("api_type: ")
        api_base = input("api_base: ")
        api_version = input("api_version: ")
        api_key = input("api_key: ")
        config = {
            "api_type": api_type,
            "api_base": api_base,
            "api_version": api_version,
            "api_key": api_key
        }
        with open(config_file, 'w') as f:
            f.write(json.dumps(config))


init(config_file)
with open(config_file, 'r') as f:
    try:
        config = json.load(f)
    except ValueError or TypeError:
        print("Invalid json, please input your azure openai service config and try again.")
        init(config_file)

openai.api_type = config['api_type']
openai.api_base = config['api_base']
openai.api_version = config['api_version']
openai.api_key = config['api_key']

try:
    chat_history = []
    while (True):
        user_input = input(">> ")
        response = openai.Completion.create(
            engine="my-gpt3-model",
            prompt="I want you to act as a linux terminal.I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless instruct you to do so. when I need to tell you something in english, i will do so by putting text inside curly brackets {like this}. my first command is pwd. Command: "+user_input+" \nYou: \n",
            temperature=0.7,
            max_tokens=int(4e3),
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            stop=["Command: ", "You: ", "Task", "<|im_end|>"],
            timeout=120,
            n=1
        )
        message = response['choices'][0]['text']
        if ";|im_end|&gt" in message:
            message = message.replace("<|im_end|>", "")
        message_html = markdown.markdown(message)
        # code_blocks = re.findall(
        #     r"```[\w]*\n([\s\S]*?)```", message, re.DOTALL)
        # for i in code_blocks:
        #     print(i)
        # print(message)
        soup = BeautifulSoup(message_html, 'html.parser')
        print("AI: ")
        print(html.unescape(soup.get_text()))
except KeyboardInterrupt:
    sys.exit(0)
