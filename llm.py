import subprocess
import os
from dotenv import load_dotenv
import re

if os.path.exists(".env"):
	load_dotenv()

EXECUTABLE_PATH = os.environ.get("EXECUTABLE_PATH")
MODEL_PATH = os.environ.get("MODEL_PATH")
PROMPT_PATH = os.environ.get("PROMPT_PATH")
RESPONSE_PATTERN = r'\[\[AI_NAME\]\]:(.*)'
WINDOW = 3

def generate_prompt(chat_history, prompt, ai="[[AI_NAME]]", human="[[USER_NAME]]"):
    output = ""
    for item in chat_history:
        output += f"{human}: {item[0]}\n{ai}: {item[1]}\n"
    output += f'{human}: {prompt}\n{ai}: '
    return output

def generate(prompt):
    with open(PROMPT_PATH, 'w') as f:
        f.write(prompt)
        f.close()
    proc = subprocess.Popen([EXECUTABLE_PATH, '-ngl', '20', '-m', MODEL_PATH, '-f', PROMPT_PATH, '-n', '4096'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW, start_new_session=True)
    while True:
        if proc.poll() is not None:
            break
    output = proc.stdout.read()
    proc.wait()
    proc.terminate()
    processed = remove_space(last_output(str(output)))
    if processed == None:
        print(output)
    return processed

def last_output(text):
    flag = False
    for num in range(len(text)):
        char = text[len(text)-1-num]
        if char == ':':
            flag = True
        elif char == ']' and flag == True:
            return text[len(text)+2-num:]
        elif flag == True:
            flag = False

def remove_space(input):
    for num in range(len(input)):
        char = input[num]
        if char != ' ' and char != '\n' and char != '\r':
            return input[num:]