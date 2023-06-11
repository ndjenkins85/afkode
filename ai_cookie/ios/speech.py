# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

import logging
import os

import speech


def speak(text):
    logging.info(f">>>{text}")
    speech.say(text, "en-US")
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)


if __name__ == "__main__":
    # Basic speech testing. Can't run as module, so we import our library here
    os.chdir("../..")
    from ai_cookie import utils

    utils.setup_logging(log_level=logging.INFO)
    speak("This is a test of the speech module")
