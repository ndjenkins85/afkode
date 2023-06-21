# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains functions related to recording speech on iOS with pythonista."""

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import console
from objc_util import *  # noqa: F403, F401
from objc_util import ObjCClass, ns


def bluetooth(file_name: str) -> Any:
    """Instanciate bluetooth audio for recording.

    Args:
        file_name: file name to convert to an apple URL

    Raises:
        ValueError: if recorder can't be started

    Returns:
        recording object
    """
    AVAudioSession = ObjCClass("AVAudioSession")
    NSURL = ObjCClass("NSURL")
    AVAudioRecorder = ObjCClass("AVAudioRecorder")
    shared_session = AVAudioSession.sharedInstance()
    category_set = shared_session.setCategory_withOptions_error_(  # noqa: F841
        ns("AVAudioSessionCategoryPlayandRecord"), 4, None
    )
    settings = {
        ns("AVFormatIDKey"): ns(1819304813),
        ns("AVSampleRateKey"): ns(22050),
        ns("AVNumberOfChannelsKey"): ns(1),
    }
    output_path = os.path.abspath(file_name)
    out_url = NSURL.fileURLWithPath_(ns(output_path))
    recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
    if recorder is None:
        console.alert("Failed to initialize recorder")
        raise ValueError  # noqa: DAR401
    return recorder


def basic_record(file_name: str, record_time: float) -> None:
    """Simple recording by time for testing.

    Args:
        file_name: file name to convert to an apple URL
        record_time: record using a sleep timer
    """
    recorder = bluetooth(file_name)
    recorder.record()
    time.sleep(record_time)
    recorder.stop()
    recorder.release()


if __name__ == "__main__":
    # Basic recording testing. Can't run as module, so we import our library here
    sys.path.append(os.path.realpath("../.."))
    from afkode import utils

    utils.setup_logging(log_level=logging.INFO)
    logging.info("Recording for 5 seconds")
    output_file_path = Path("..", "..", "data", "detect_stop", "basic_record_test.wav")
    basic_record(str(output_file_path), 5)
    logging.info(f"Saved recording to {output_file_path}")
