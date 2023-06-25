# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file is the main entry point of the AFKode program.

It handles the execution of the program and orchestrates the different components.
"""

import logging
from datetime import datetime as dt
from pathlib import Path

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env  # noqa: F401

    from afkode.ios.speech import speak
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401
    from afkode.macos.speech import speak

from afkode import action, api, utils, voice_interface


def start() -> None:
    """Begins the AFKode program and handles the user interaction and file operations.

    The program records voice input, transcribes it, and performs various operations based on the user's commands.

    It includes the main program loop, which only exits when specifically commanded by the user.
    """
    while True:
        # for i in ["1"]: # for debug purposes
        speak("Recording")
        recorder = voice_interface.VoiceRecorder()
        recorder.clear_data()
        recorder.start_detection()
        speak("Stopped")

        transcription = recorder.transcribe_whole()
        logging.info(transcription)

        # Soft exit using a very short transcription
        exit_test = utils.split_transcription_on(transcription, words="exit", strategy="detect")
        if len(exit_test) < len(transcription) and len(transcription) < 21:
            speak("Exiting")
            break

        # Commands
        resolved = action.Command(transcription)
        if resolved.command:
            speak(resolved.command.replace("_", " "))
            result = resolved.execute()
            speak(result)

        # It could be that the command wasn't recognised and we dont want it to be recorded like that
        elif len(transcription) < 21:
            speak("Skipping")
        else:
            # Otherwise it's not a command
            proposed_filename_prompt = Path(utils.get_prompt_path(), "programflow", "proposed_filename.txt").read_text()

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
