import threading
import os
import shutil
import time
# you would need to import the appropriate modules for audio recording and transcription

from api import whisper, chatgpt
from apple import iphone_bluetooth_record
from globals import stop_threads

class VoiceRecorder:
    def __init__(self):
        pass

    def continuous_recording(self):
        # Implement continuous recording here
        while not stop_threads:
            # record continuously

    def periodic_recording(self):
        file_counter = 1
        while not stop_threads:
            # record for 3 seconds
            # save recording to file "detection" + str(file_counter).zfill(4) + ".wav"
            file_counter += 1
            time.sleep(3)

    def transcribe_and_detect_stop(self):
        while not stop_threads:
            # check for new files in 'input' folder
            # transcribe new files
            # if transcription contains 'stop', self.recording = False

    def start(self):
        # clear input and output folders
        shutil.rmtree('data/inputs')
        shutil.rmtree('data/outputs')
        os.mkdir('data/inputs')
        os.mkdir('data/outputs')

        # start threads
        threading.Thread(target=self.continuous_recording).start()
        threading.Thread(target=self.periodic_recording).start()
        threading.Thread(target=self.transcribe_and_detect_stop).start()


recorder = VoiceRecorder()
recorder.start()
