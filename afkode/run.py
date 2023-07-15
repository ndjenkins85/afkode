# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file is the main entry point of the AFKode program.

It handles the execution of the program and orchestrates the different components.
"""

import logging

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env  # noqa: F401

    from afkode.ios.speech import speak
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401
    from afkode.macos.speech import speak

from afkode import action, utils, voice_interface
from afkode.commands import summarize_filename


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

        transcript = recorder.transcribe_whole()
        logging.info(transcript)

        # Soft exit using a very short transcript
        exit_test = utils.split_transcription_on(transcript, words="exit", strategy="detect")
        if len(exit_test.strip()) < len(transcript.strip()) and len(transcript) < 21:
            speak("Exiting")
            break

        # Checks if it is a command
        resolved = action.Command(transcript)
        if resolved.command:
            speak(resolved.command.replace("_", " "))
            result = resolved.execute()
            speak(result)
        # It could be that the command wasn't recognised and we dont want it to be recorded like that
        elif len(transcript) < 21:
            speak("Skipping")
        # Otherwise use the default command to summarize_filename and save transcript
        else:
            proposed_filename = summarize_filename.execute(transcript)
            speak(proposed_filename)


if __name__ == "__main__":
    utils.setup_logging()
    start()
