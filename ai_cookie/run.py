# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""This script runs the user input loop."""
import logging
from pathlib import Path

from api import chatgpt
from file import FileIO
from globals import *
from voice_alt import VoiceRecorder

from ai_cookie import utils


def start():
    utils.running_on_pythonista()

    io = FileIO()
    while True:
        utils.speak("Recording")

        global stop_threads
        stop_threads = False
        recorder = VoiceRecorder()
        recorder.clear_data()
        recorder.start_detection()

        print("test for early end")
        transcription = recorder.transcribe_whole()

        command = io.command(transcription)
        if command == "exit":
            utils.speak("Exiting")
            break
        # Confirm destructive commands
        elif command == "confirm":
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
        prompt_user_input_assist = Path("..", "prompts", "programflow", "user_input_assist.txt").read_text()
        prompt_user_input_assist += "\n" + transcription

        # TODO need to create the actual chat loop with ongoing conversation elements
        response = chatgpt(prompt_user_input_assist)

        io.latest_response = response

        utils.speak(response)


if __name__ == "__main__":
    utils.setup_logging()
    start()
