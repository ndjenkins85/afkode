# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This script runs the user input loop."""

import logging
from pathlib import Path

from ai_cookie import utils

utils.setup_logging(log_level=logging.INFO)
if utils.running_on_pythonista():
    from ai_cookie.ios.speech import speak
else:
    from ai_cookie.macos.speech import speak

from ai_cookie import api, file, voice_alt


def start():
    io = file.FileIO()
    # while True:
    for i in ["1"]:
        speak("Recording")
        recorder = voice_alt.VoiceRecorder()
        recorder.clear_data()
        recorder.start_detection()
        speak("Stopped")

        transcription = recorder.transcribe_whole()
        logging.info(transcription)

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
        proposed_filename_prompt = Path("prompts", "programflow", "proposed_filename.txt").read_text()

        # TODO, surely there is a template approach to prompts?
        proposed_filename_prompt += (
            "\n" + utils.get_user_prompt_files() + "\n\n--------- Here is the user input:\n" + transcription
        )
        logging.debug(proposed_filename_prompt)
        proposed_filename_response = api.chatgpt(proposed_filename_prompt)
        speak(proposed_filename_response)
        io.save_response(transcription, proposed_filename_response)


if __name__ == "__main__":
    start()
