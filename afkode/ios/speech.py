# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains functions related to text-to-speech on iOS with pythonista."""

import logging
import os
import sys
import time

import speech

# import sound


def speak(text: str) -> None:
    """Say the text using iOS capability.

    Args:
        text: text to say
    """
    logging.info(f">>>{text}")
    speech.say(text, "en-US")
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)


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
