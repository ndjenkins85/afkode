"""This script runs the user input loop."""
from pathlib import Path

from voice_alt import VoiceRecorder
from file import FileIO
from globals import *
from api import chatgpt

io = FileIO()
while True:
    utils.speak("Recording")
    
    global stop_threads
    stop_threads = False
    transcription = VoiceRecorder().start_threads().transcribe_whole()

    command = io.command(transcription)
    if command = "exit":
        utils.speak("Exiting")
        break
    # Confirm destructive commands
    elif command = "confirm":
        utils.speak("Confirm command")
        transcription = VoiceRecorder().simple_record()
        confirm = io.confirm(transcription)
        if confirm:
            utils.speak("Confirmed")
            break
        else:
            utils.speak("Continuing")
            continue        
    elif command:
        utils.speak(command)
        continue

    # Otherwise it's not a command
    prompt_user_input_assist = Path('..', 'prompts', 'programflow', 'user_input_assist.txt').read()
    prompt_user_input_assist += "\n" + transcription

    # TODO need to create the actual chat loop with ongoing conversation elements
    response = chatgpt(prompt_user_input_assist)
    
    io.latest_response = response
    
    # TODO make util
    utils.speak(response)
