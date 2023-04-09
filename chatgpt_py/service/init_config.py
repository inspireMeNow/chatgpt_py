import os
import openai
import json
import platform



def check_system():
    if platform.system() == 'Windows':
        return os.getenv('HOMEPATH')+'\\.config\\chatgpt-py'
    else:
        return os.getenv('HOME')+'/.config/chatgpt-py'

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
