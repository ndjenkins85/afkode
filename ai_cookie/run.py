# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file is the main entry point of the AFKode program.

It handles the execution of the program and orchestrates the different components.
"""

import logging
from pathlib import Path

from ai_cookie import utils

utils.setup_logging(log_level=logging.INFO)
if utils.running_on_pythonista():
    from ai_cookie.ios.speech import speak
else:
    from ai_cookie.macos.speech import speak

from ai_cookie import api, voice_interface


def start() -> None:
    """Begins the AFKode program and handles the user interaction and file operations.

    The program records voice input, transcribes it, and performs various operations based on the user's commands.
    """
    while True:
        # for i in ["1"]: # for debug purposes
        speak("Recording")
        recorder = voice_alt.VoiceRecorder()
        recorder.clear_data()
        recorder.start_detection()
        speak("Stopped")

        transcription = recorder.transcribe_whole()
        logging.info(transcription)

        if transcription.lower()[:4] == "exit":
            speak("Exiting")
            break

        # Otherwise it's not a command
        proposed_filename_prompt = Path("prompts", "programflow", "proposed_filename.txt").read_text()

        # TODO, surely there is a template approach to prompts?
        proposed_filename_prompt += (
            "\n" + utils.get_user_prompt_files() + "\n\n--------- Here is the user input:\n" + transcription
        )
        logging.debug(proposed_filename_prompt)
        proposed_filename_response = api.chatgpt(proposed_filename_prompt)
        speak(proposed_filename_response)
        output_path = Path(utils.get_user_prompt_directory(), f"{dt.now()} - {proposed_filename_response}.txt")
        output_path.write_text(transcription, encoding="utf-8")


if __name__ == "__main__":
    start()
