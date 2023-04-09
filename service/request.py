import json
import openai
import sys
import markdown
from bs4 import BeautifulSoup
import html
import re
import os
from cli_input import *
from prompt import change_style
import traceback

config_azure_file = os.getenv('HOME')+'/.config/chatgpt-py/config_azure.json'
config_openai_file = os.getenv('HOME')+'/.config/chatgpt-py/config_openai.json'


def init_azure(config_azure_file):
    if not os.path.exists(config_azure_file):
        api_type = input("api_type: ")
        api_base = input("api_base: ")
        api_version = input("api_version: ")
        api_key = input("api_key: ")
        engine = input("engine: ")
        max_tokens = input("max_tokens: ")
        temperature = input("temperature: ")
        timeout = input("timeout: ")
        config = {
            "api_type": api_type,
            "api_base": api_base,
            "api_version": api_version,
            "api_key": api_key,
            "engine": engine,
            "max_tokens": int(float(max_tokens)),
            "temperature": float(temperature),
            "timeout": int(timeout)
        }
        os.system("mkdir -p "+os.getenv('HOME')+'/.config/chatgpt-py')
        with open(config_azure_file, 'w') as f:
            f.write(json.dumps(config))


def init_openai(config_openai_file):
    if not os.path.exists(config_openai_file):
        api_key = input("api_key: ")
        openai.api_key = api_key
        i = 0
        available_engine = []
        available_list = openai.Engine.list()['data']
        while (i < len(available_list)):
            available_engine.append(available_list[i]['id'])
            i += 1
        print("Available engines:")
        i = 0
        while i < len(available_engine):
            print("\033[92m" + str(i+1) + "\033[0m", end=": ")
            print(available_engine[i])
            i += 1
        engine = input("\033[92m" +
                       "Which engine would you like to use? \n" + "\033[0m")
        engine = available_engine[int(engine)-1]
        max_tokens = input("max_tokens: ")
        temperature = input("temperature: ")
        timeout = input("timeout: ")
        config = {
            "api_type": "openai",
            "api_key": api_key,
            "engine": engine,
            "max_tokens": int(float(max_tokens)),
            "temperature": float(temperature),
            "timeout": int(timeout)
        }
        os.system("mkdir -p "+os.getenv('HOME')+'/.config/chatgpt-py')
        with open(config_openai_file, 'w') as f:
            f.write(json.dumps(config))


api_type = ia_selection("What's your OpenAI API type?",
                        options=["Azure", "OpenAI"],
                        flags=[f"~",
                               f"~"])
match(api_type):
    case "Azure":
        init_azure(config_azure_file)
        with open(config_azure_file, 'r') as f:
            try:
                config = json.load(f)
            except ValueError or TypeError:
                print(
                    "Invalid json, please input your azure openai service config and try again.")
                init_azure(config_azure_file)

        openai.api_type = config['api_type']
        openai.api_base = config['api_base']
        openai.api_version = config['api_version']
        openai.api_key = config['api_key']
    case "OpenAI":
        init_openai(config_openai_file)
        with open(config_openai_file, 'r') as f:
            try:
                config = json.load(f)
            except ValueError or TypeError:
                print(
                    "Invalid json, please input your openai service config and try again.")
                init_openai(config_openai_file)
        openai.api_key = config['api_key']

try:
    messages = []
    character = ia_selection("Which AI character would you like to use?",
                             options=["Linux Terminal", "Helpful Assistant"],
                             flags=[f"~",
                                    f"~"])
    prompt = change_style(character)
    while (True):
        user_input = input(">> ")
        messages.append(
            {"role": "user", "content": prompt[1]+"user: "+user_input+" "+prompt[0]+": "})
        response = openai.ChatCompletion.create(
            engine=config['engine'] if config['api_type'] == "azure" else None,
            model=config['engine'] if config['api_type'] == "openai" else None,
            messages=messages,
            temperature=config['temperature'],
            max_tokens=int(config['max_tokens']),
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            stop=["user: ", prompt[0]+": ", "<|im_end|>"],
            timeout=int(config['timeout'])
        )
        chat_response = response
        answer = chat_response['choices'][0]['message']['content']
        if ";|im_end|&gt" in answer:
            answer = answer.replace("<|im_end|>", "")
        answer_html = markdown.markdown(answer)
        # code_blocks = re.findall(
        #     r"```[\w]*\n([\s\S]*?)```", answer, re.DOTALL)
        # for i in code_blocks:
        #     print(i)
        # print(answer)
        soup = BeautifulSoup(answer_html, 'html.parser')
        print(prompt[0]+f': \n{html.unescape(soup.get_text())}')
        messages.append(
            {"role": prompt[0], "content": html.unescape(soup.get_text())})
except Exception or KeyboardInterrupt:
    traceback.print_exc()
    sys.exit(0)
