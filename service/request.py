import json
import openai
import sys
import markdown
from bs4 import BeautifulSoup
import html
import re
import os
import atexit
import tty
import termios
from itertools import zip_longest
from prompt import change_style

config_file = os.getenv('HOME')+'/.config/chatgpt-py/config.json'


class KeyGetter:
    def arm(self):
        self.old_term = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        atexit.register(self.disarm)

    def disarm(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_term)

    def getch(self):
        self.arm()
        ch = sys.stdin.read(1)[0]
        self.disarm()
        return ch


def print_question(message: str) -> None:
    print("\033[92m" + message + "\033[0m", flush=True)


def ia_selection(question: str, options: list = None, flags: list = None) -> str:
    print_question(question)
    return _draw_ia_selection(options, flags)


def _draw_ia_selection(options: list, flags: list = None):
    __UNPOINTED = " "
    __POINTED = ">"
    __INDEX = 0
    __LENGTH = len(options)
    __ARROWS = __UP, _ = 65, 66
    __ENTER = 10

    if flags is None:
        flags = []

    def _choices_print():
        for i, (option, flag) in enumerate(zip_longest(options, flags, fillvalue='')):
            if i == __INDEX:
                print(f" {__POINTED} {{0}}{option} {flag}{{1}}".format(
                    '\033[94m', '\033[0m'))
            else:
                print(f" {__UNPOINTED} {option} {flag}")

    def _choices_clear():
        print(f"\033[{__LENGTH}A\033[J", end='')

    def _move_pointer(ch_ord: int):
        nonlocal __INDEX
        __INDEX = max(
            0, __INDEX - 1) if ch_ord == __UP else min(__INDEX + 1, __LENGTH - 1)

    def _main_loop():
        kg = KeyGetter()
        _choices_print()
        while True:
            key = ord(kg.getch())
            if key in __ARROWS:
                _move_pointer(key)
            _choices_clear()
            _choices_print()
            if key == __ENTER:
                _choices_clear()
                _choices_print()
                break

    _main_loop()
    return options[__INDEX]


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
        os.system("mkdir -p "+os.getenv('HOME')+'/.config/chatgpt-py')
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
            engine="my-gpt3-model",
            messages=messages,
            temperature=0.7,
            max_tokens=int(4e3),
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            stop=["user: ", prompt[0]+": ", "Task: ", "<|im_end|>"],
            timeout=120,
            n=1
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
except KeyboardInterrupt:
    sys.exit(0)
