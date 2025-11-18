import os
import json
import time
import sys
from typing import Union, List
sys.path.append('outputs/scripts')
from unified_api import UnifiedAPI


def get_env_variable(var_name):
    """Fetch environment variable or return None if not set."""
    return os.getenv(var_name)

CALL_SLEEP = 1

def get_client(model_name):
    return UnifiedAPI(model_name)

def read_prompt_from_file(filename):
    with open(filename, 'r') as file:
        prompt = file.read()
    return prompt

def read_data_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def parse_json(output):
    try:
        output = ''.join(output.splitlines())
        if '{' in output and '}' in output:
            start = output.index('{')
            end = output.rindex('}')
            output = output[start:end + 1]
        data = json.loads(output)
        return data
    except Exception as e:
        print("parse_json:", e)
        return None
    
def check_file(file_path):
    if os.path.exists(file_path):
        return file_path
    else:
        raise IOError(f"File not found error: {file_path}.")

def gpt_call(client, query: Union[List, str], model_name = "gpt-4o", temperature = 0):
    if isinstance(query, List):
        messages = query
    elif isinstance(query, str):
        messages = [{"role": "user", "content": query}]
    for _ in range(3):
        try:
            resp = client.call(
                    messages=messages,
                    temperature=temperature
                )
            return resp
        except Exception as e:
            print(f"GPT_CALL Error: {model_name}:{e}")
            time.sleep(CALL_SLEEP)
            continue
    return ""

def gpt_call_append(client, model_name, dialog_hist: List, query: str):
    dialog_hist.append({"role": "user", "content": query})
    resp = gpt_call(client, dialog_hist, model_name=model_name)
    dialog_hist.append({"role": "assistant", "content": resp})
    return resp, dialog_hist
