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

import os
import time

import console
from globals import stop_threads
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
        print(">>>RECORDER IS NONE")
        console.alert("Failed to initialize recorder")
        raise ValueError
        return None
    return recorder


def iphone_bluetooth_record(file_name, record_time):
    recorder = bluetooth(file_name)
    recorder.record()
    for i in range(record_time * 4):
        time.sleep(0.25)
        if stop_threads:
            return None
    recorder.stop()
    recorder.release()
