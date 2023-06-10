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

from ai_cookie import utils

utils.setup_logging()
if utils.running_on_pythonista():
    from ai_cookie.ios.speech import speak
else:
    from ai_cookie.macos.speech import speak

from ai_cookie import api, file, voice_alt
from ai_cookie.globals import *


def start():
    io = file.FileIO()
    while True:
        speak("Recording")

        global stop_threads
        stop_threads = False
        recorder = voice_alt.VoiceRecorder()
        recorder.clear_data()
        recorder.start_detection()

        transcription = recorder.transcribe_whole()

        # 1/0

        # command = io.command(transcription)
        # if command == "exit":
        #     speak("Exiting")
        #     break
        # # Confirm destructive commands
        # elif command == "confirm":
        #     speak("Confirm command")
        #     transcription = voice_alt.VoiceRecorder().simple_record()
        #     confirm = io.confirm(transcription)
        #     if confirm:
        #         speak("Confirmed")
        #         break
        #     else:
        #         speak("Continuing")
        #         continue
        # elif command:
        #     speak(command)
        #     continue

        # Otherwise it's not a command
        prompt_user_input_assist = Path("prompts", "programflow", "user_input_assist.txt").read_text()
        prompt_user_input_assist += "\n" + transcription

        # TODO need to create the actual chat loop with ongoing conversation elements
        response = api.chatgpt(prompt_user_input_assist)

        io.latest_response = response

        speak(response)


if __name__ == "__main__":
    utils.setup_logging()
    start()
