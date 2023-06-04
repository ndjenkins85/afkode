"""This script runs the user input loop."""
from pathlib import Path

from voice_alt import VoiceRecorder
from file import FileIO
from globals import *
from api import chatgpt
from utils import speak

io = FileIO()
while True:
    speak("Recording")
    
    global stop_threads
    stop_threads = False
    recorder = VoiceRecorder()
    recorder.clear_data()
    recorder.start_detection()
    transcription = recorder.transcribe_whole()

    command = io.command(transcription)
    if command == "exit":
        speak("Exiting")
        break
    # Confirm destructive commands
    elif command == "confirm":
        speak("Confirm command")
        transcription = VoiceRecorder().simple_record()
        confirm = io.confirm(transcription)
        if confirm:
            speak("Confirmed")
            break
        else:
            speak("Continuing")
            continue        
    elif command:
        speak(command)
        continue

    # Otherwise it's not a command
    prompt_user_input_assist = Path('..', 'prompts', 'programflow', 'user_input_assist.txt').read_text()
    prompt_user_input_assist += "\n" + transcription

    # TODO need to create the actual chat loop with ongoing conversation elements
    response = chatgpt(prompt_user_input_assist)
    
    io.latest_response = response
    
    speak(response)
