import json
import openai
import sys
import markdown
from bs4 import BeautifulSoup
import html
import re
import os
from chatgpt_py.service.init_config import *
from chatgpt_py.service.prompt import change_style

config_azure_file = check_system() + "/config_azure.json"
config_openai_file = check_system() + '/config_openai.json'


def select_prompt():
    from chatgpt_py.service.cli_input import ia_selection
    if platform.system() == 'Windows':
        print(
            "\033[92m" + "Which AI character would you like to use?" + "\033[0m")
        print(
            "\033[94m" + "\t1. Linux Terminal\n\t2. Helpful Assistant\n\t3. Translator in English\n\t4. "
                         "Translator\n\t5. Others\n\t6. Exit" + "\033[0m")
        number = input("\033[100m" + ">> " + "\033[0m")
        character = ''
        while True:
            match number:
                case "1":
                    character = "Linux Terminal"
                case "2":
                    character = "Helpful Assistant"
                case "3":
                    character = 'Translator in English'
                case "4":
                    character = 'Translator'
                case "5":
                    character = 'Others'
                case "6":
                    sys.exit(0)
                case _:
                    print("Invalid input, please try again.")
                    number = input("\033[100m" + ">> " + "\033[0m")
    else:
        character = ia_selection("Which AI character would you like to use? You can also choose Exit to exit the "
                                 "program.",
                                 options=["Linux Terminal",
                                          "Helpful Assistant",
                                          "Translator in English",
                                          "Translator",
                                          "Others",
                                          "Exit"],
                                 flags=[f"~",
                                        f"~",
                                        f"~",
                                        f"~",
                                        f"~",
                                        f"~"])
    if character == 'Exit':
        sys.exit(0)
    return character


def main():
    if platform.system() == 'Windows':
        print("\033[92m" + "What's your OpenAI API type?" + "\033[0m")
        print("\033[94m" + "\t1. Azure\n\t2. OpenAI" + "\033[0m")
        number = input("\033[100m" + ">> " + "\033[0m")
        while True:
            match number:
                case "1":
                    api_type = "Azure"
                case "2":
                    api_type = "OpenAI"
                case _:
                    print("Invalid input, please try again.")
                    number = input("\033[100m" + ">> " + "\033[0m")
    else:
        from chatgpt_py.service.cli_input import ia_selection
        api_type = ia_selection("What's your OpenAI API type?",
                                options=["Azure", "OpenAI"],
                                flags=[f"~",
                                       f"~"])
    match api_type:
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

    selected_prompt = ''
    selected_prompt = select_prompt()
    while True:
        prompt = change_style(selected_prompt)
        messages = []
        try:
            while True:
                try:
                    user_input = input("\033[100m" + ">> " + "\033[0m")
                    messages.append(
                        {"role": "user", "content": prompt[1] + "user: " + user_input + " " + prompt[0] + ": "})
                    response = openai.ChatCompletion.create(
                        engine=config['engine'] if config['api_type'] == "azure" else None,
                        model=config['engine'] if config['api_type'] == "openai" else None,
                        messages=messages,
                        temperature=config['temperature'],
                        max_tokens=int(config['max_tokens']),
                        # top_p=1,
                        # frequency_penalty=0,
                        # presence_penalty=0,
                        stop=["user: ", prompt[0] + ": ", "<|im_end|>"],
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
                    print(prompt[0] + f': \n{html.unescape(soup.get_text())}')
                    messages.append(
                        {"role": prompt[0], "content": html.unescape(soup.get_text())})
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))
        except KeyboardInterrupt:
            selected_prompt = select_prompt()
