import speech_recognition as sr
import pyttsx3
from urllib import request

def speech_text():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)                
            audio2 = r.listen(source2)
            if internet_on():
                text = r.recognize_google(audio2)
                print('a')
            else:
                text = r.recognize_sphinx(audio2)
            text = text.lower()
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None
    except sr.UnknownValueError:
        return None
    return text

def speak_text(command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

def internet_on():
    try:
        request.urlopen('http://1.1.1.1', timeout=1)
        return True
    except request.URLError as err: 
        return False