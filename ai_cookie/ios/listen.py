# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

import os
import time

import console
from objc_util import *


def bluetooth(file_name):
    """Instanciate bluetooth audio for recording."""
    AVAudioSession = ObjCClass("AVAudioSession")
    NSURL = ObjCClass("NSURL")
    AVAudioRecorder = ObjCClass("AVAudioRecorder")
    shared_session = AVAudioSession.sharedInstance()
    category_set = shared_session.setCategory_withOptions_error_(ns("AVAudioSessionCategoryPlayandRecord"), 4, None)
    settings = {
        ns("AVFormatIDKey"): ns(1819304813),
        ns("AVSampleRateKey"): ns(44100.0),
        ns("AVNumberOfChannelsKey"): ns(1),
    }
    output_path = os.path.abspath(file_name)
    out_url = NSURL.fileURLWithPath_(ns(output_path))
    recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
    if recorder is None:
        console.alert("Failed to initialize recorder")
        raise ValueError
        return None
    return recorder


def basic_record(file_name, record_time):
    recorder = bluetooth(file_name)
    recorder.record()
    time.sleep(record_time)
    recorder.stop()
    recorder.release()


if __name__ == "__main__":
    # Can run this module directly for basic recording testing
    output_file_path = Path("data", "detect_stop", "basic_record_test.wav")
    basic_record(str(output_file_path), 5)
