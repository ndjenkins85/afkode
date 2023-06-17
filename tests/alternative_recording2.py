# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

import datetime

import ui
from objc_util import *

AVAudioEngine = ObjCClass("AVAudioEngine").alloc().init()
AVAudioSession = ObjCClass("AVAudioSession")
AVAudioRecorder = ObjCClass("AVAudioRecorder")

shared_session = AVAudioSession.sharedInstance()
category_set = shared_session.setCategory_withOptions_error_(
    ns("AVAudioSessionCategoryRecord"), 0x2, None  # duckothers
)
shared_session.setMode_error_(ns("AVAudioSessionModeMeasurement"), None)

setActiveOptions = 0  # notifyOthersOnDeactivation
shared_session.setActive_withOptions_error_(True, setActiveOptions, None)

inputNode = AVAudioEngine.inputNode()

# Configure the microphone input.
recordingFormat = inputNode.outputFormatForBus_(0)

# Create and configure the speech recognition request.
recognitionRequest = ObjCClass("SFSpeechAudioBufferRecognitionRequest").alloc().init()
recognitionRequest.setShouldReportPartialResults_(True)
retain_global(recognitionRequest)


@on_main_thread
def handler_buffer(_cmd, obj1_ptr, obj2_ptr):
    # print('handler_buffer',datetime.datetime.now())
    # param1 = AVAudioPCMBuffer
    #   The buffer parameter is a buffer of audio captured
    #   from the output of an AVAudioNode.
    # param2 = AVAudioTime
    #   The when parameter is the time the buffer was captured
    if obj1_ptr:
        obj1 = ObjCInstance(obj1_ptr)
        # print(str(obj1._get_objc_classname())) # AVAudioPCMBuffer
        # print(str(obj1.frameLength()))                 # 4410
        # segmentation in next line if no "_" before appendAudioPCMBuffer
        recognitionRequest._appendAudioPCMBuffer_(obj1)


handler_block_buffer = ObjCBlock(handler_buffer, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])

inputNode.installTapOnBus_bufferSize_format_block_(0, 1024, recordingFormat, handler_block_buffer)

AVAudioEngine.prepare()
err_ptr = c_void_p()
AVAudioEngine.startAndReturnError_(byref(err_ptr))
if err_ptr:
    err = ObjCInstance(err)
    print(err)


# @on_main_thread
def handler_recognize(_cmd, obj1_ptr, obj2_ptr):
    # print('handler_recognize')
    # param1 = result
    #                   The object containing the partial/final transcriptions
    #                   of the audio content.
    # param2 = error
    #                       An error object if a problem occurred.
    #                       This parameter is nil if speech recognition was successful.
    if obj1_ptr:
        obj1 = ObjCInstance(obj1_ptr)
        # obj1 is a SFSpeechRecognitionResult
        print(obj1.bestTranscription().formattedString())


handler_block_recognize = ObjCBlock(handler_recognize, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])

SFSpeechRecognizer = ObjCClass("SFSpeechRecognizer").alloc().init()
recognitionTask = SFSpeechRecognizer.recognitionTaskWithRequest_resultHandler_(
    recognitionRequest, handler_block_recognize
)

mv = ui.View()
b = ui.ButtonItem()
b.title = "stop"


def b_stop(sender):
    AVAudioEngine.stop()
    recognitionRequest.endAudio()


b.action = b_stop
mv.right_button_items = (b,)
mv.present("sheet")
