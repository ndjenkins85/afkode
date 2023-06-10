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

import logging
import time
from pathlib import Path

import speech
from globals import *


def speak(text):
    global debug
    if debug:
        print(f">>>{text}")
    speech.say(text, "en-US")
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)


def setup_logging() -> None:
    """Setup basic logging to path."""
    log_path = Path("logs", "_log.txt")
    log_level = logging.DEBUG

    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f"""Directory '{log_path}' missing, cannot create log file.
                  Make sure you are running from base of repo, with correct data folder structure.
                  Continuing without log file writing."""
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)


def running_on_pythonista() -> bool:
    try:
        import console

        logging.debug(">>Running on pythonista")
        return True
    except ModuleNotFoundError:
        logging.debug(">>Running on standard compute")
        return False
