from llm import generate
from llm import generate_prompt
from llm import WINDOW
from speach import speech_text
from speach import speak_text

def chat():
    chat_history = []
    while True:
        raw_prompt = ""
        while True:
            raw_prompt = speech_text()
            if raw_prompt != None:
                break
        print(raw_prompt)
        if raw_prompt == "quit":
            return
        prompt = generate_prompt(chat_history, raw_prompt)
        response = generate(prompt)
        print(response)
        speak_text(response)
        chat_history.append((raw_prompt, response))
        if len(chat_history) > WINDOW:
            chat_history = chat_history[1:]

if __name__ == "__main__":
    chat()
