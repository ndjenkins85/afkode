# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains functions related to text-to-speech on iOS with pythonista."""

import logging
import os
import sys
import time
from pathlib import Path

import sound
import speech

from afkode import api


def speak_old(text: str) -> None:
    """Say the text using iOS capability.

    Args:
        text: text to say
    """
    logging.info(f">>>{text}")
    speech.say(text, "en-US")
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)


def speak(text: str) -> None:
    """Run text-to-speech on ios platform.

    Args:
        text: full text to be spoken.
    """
    tts_base_path = Path(utils.get_base_path(), "data", "text_to_speech")
    if not tts_base_path.exists():
        tts_base_path.mkdir(parents=True)
    logging.info(f">>>{text}")

    # Attempt to use cache if couple of words or is a command
    if len(text.split(" ")) <= 2 or text in utils.get_spoken_command_list():
        tts_path = Path(tts_base_path, f"{text}.wav")
        if tts_path.exists():
            sound.play(tts_path)
            return None
    else:
        tts_path = Path(tts_base_path, f"latest.wav")

    api.google_tts(tts_path, text_input=text)
    sound.play(tts_path)


def play_blip() -> None:
    """Play a short sound to help notify of API speed."""
    # sound.play_effect("ui:mouseclick1")
    pass


if __name__ == "__main__":
    # Basic speech testing. Can't run as module, so we import our library here
    sys.path.append(os.path.realpath("../.."))
    from afkode import utils

    utils.setup_logging(log_level=logging.INFO)
    speak("This is a test of the speech module")
