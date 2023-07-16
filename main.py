import subprocess
import os
from dotenv import load_dotenv
import re

if os.path.exists(".env"):
	load_dotenv()

EXECUTABLE_PATH = os.environ.get("EXECUTABLE_PATH")
MODEL_PATH = os.environ.get("MODEL_PATH")
PROMPT_PATH = os.environ.get("PROMPT_PATH")
RESPONSE_PATTERN = r'\[\[AI_NAME\]\](.*)'


def talk():
    while True:
        prompt = input()
        if prompt == "quit":
            return
        prompt = f"[[USER_NAME]]: {prompt}\n[[AI_NAME]]: "
        print(generate(prompt))

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
    return re.search(RESPONSE_PATTERN, output.decode('utf-8')).group(1)[3:]

if __name__ == "__main__":
    talk()
