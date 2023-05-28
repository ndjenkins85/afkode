import time
import os

import console
from objc_util import *

from globals import stop_threads

def bluetooth(file_name):
    """Instanciate bluetooth audio for recording."""
    AVAudioSession = ObjCClass('AVAudioSession')
    NSURL = ObjCClass('NSURL')
    AVAudioRecorder = ObjCClass('AVAudioRecorder')
    shared_session = AVAudioSession.sharedInstance()
    category_set = shared_session.setCategory_withOptions_error_(ns('AVAudioSessionCategoryPlayandRecord'), 4, None)
    settings = {
        ns('AVFormatIDKey'): ns(1819304813),
        ns('AVSampleRateKey'):ns(44100.0),
        ns('AVNumberOfChannelsKey'):ns(1)
    }
    output_path = os.path.abspath(file_name)
    out_url = NSURL.fileURLWithPath_(ns(output_path))
    recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
    if recorder is None:
        print(">>>RECORDER IS NONE")
        console.alert('Failed to initialize recorder')
        raise ValueError
        return None
    return recorder

def iphone_bluetooth_record(file_name, record_time):
    recorder = bluetooth(file_name)
    recorder.record()
    for i in range(record_time*4):
        time.sleep(0.25)
        if stop_threads:
            return None
    recorder.stop()
    recorder.release()
