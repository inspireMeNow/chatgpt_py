import json
import openai
import sys
import markdown
from bs4 import BeautifulSoup
import html
import re
import os

openai.api_type = os.environ.get('OPENAI_API_TYPE')
openai.api_base = os.environ.get('OPENAI_API_BASE')
openai.api_version = os.environ.get('OPENAI_API_VERSION')
openai.api_key = os.environ.get('OPENAI_API_KEY')

try:
    chat_history = []
    while (True):
        user_input = input(">> ")
        response = openai.Completion.create(
            engine="my-gpt3-model",
            prompt="User: "+user_input+" \nAI: \n",
            temperature=0.9,
            max_tokens=int(4e3),
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            stop=["User: ", "AI: ", "<|im_end|>"],
            timeout=300,
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
