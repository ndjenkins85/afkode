import speech

from global import *

def speak(text):
    global debug
    if debug:
        print(f">>>{text}")
    speech.say(text, 'en-US')    
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)

