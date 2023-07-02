# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Attempts to check both speaking and listening to ensure both services work together."""

import logging
import tempfile
import time
from pathlib import Path

import set_env  # noqa: F401

from afkode.ios.listen import bluetooth
from afkode.ios.speech import speak

sys.path.append(os.path.realpath("../.."))

logging.info("Recording for 5 seconds")
output_file_path = Path("..", "..", "data", "detect_stop", "basic_record_test.wav")
basic_record(str(output_file_path), 5)
logging.info(f"Saved recording to {output_file_path}")

speak("This is a test of the speech module")

basic_record(str(output_file_path), 5)
logging.info(f"Saved recording to {output_file_path}")
