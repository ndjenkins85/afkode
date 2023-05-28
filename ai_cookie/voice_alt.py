import threading
import os
import shutil
import time
from pathlib import Path

#from mock_api import whisper, chatgpt
from api import whisper, chatgpt
from apple import iphone_bluetooth_record, bluetooth
from globals import *


class VoiceRecorder:
    def __init__(self):
        self.folder_base = Path('..', 'data', 'detect_stop')
        self.whole_folder = Path(self.folder_base, 'whole')
        self.short_folder = Path(self.folder_base, 'short')
        self.transcript_folder = Path(self.folder_base, 'transcript')
        self.file_ext = ".wav"
        self.short_time = 3
        self.simple_wait = 3
        self.tick = 0.2
        self.stop_word = " stop"
        self.clear_data()
       
    def whole_recording(self):
        """This produces the primary audio file for whole transcription later."""
        global stop_threads        
        file_name = Path(self.whole_folder, "whole" + self.file_ext)
        recorder = bluetooth(str(file_name))
        recorder.record()
        while not stop_threads:
            time.sleep(self.tick)
        #time.sleep(7)
        recorder.stop()
        recorder.release()

    def short_recording(self):
        """We use shorter recordings for stop word detection every few seconds."""
        global stop_threads
        time.sleep(1) # Add a slight delay for the recording
        file_counter = 1
        while not stop_threads:
            file_name = Path(self.short_folder, "short" + str(file_counter).zfill(4) + self.file_ext)
            recorder = bluetooth(str(file_name))
            recorder.record()
            for i in range(int(self.short_time / self.tick)):
                time.sleep(self.tick)
                if stop_threads:
                    break
            recorder.stop()
            recorder.release()
            file_counter += 1

    def transcribe_and_detect_stop(self):
        """This process looks for short recordings, transcribes, and looks for stopwords then signals to stop threads."""
        global stop_threads
        global debug
        while not stop_threads:
            # Get the list of input files and output files, ignoring latest partial recording
            time.sleep(self.short_time - self.tick)      
            input_files = sorted(os.listdir(self.short_folder))[:-1]
            output_files = os.listdir(self.transcript_folder)            

            # Check each input file
            for file_name in input_files:
                # If this file hasn't been transcribed yet
                if f'{file_name}.txt' not in output_files:
                    short_path = Path(self.short_folder, file_name)
                    transcribe_path = Path(self.transcript_folder, f'{file_name}.txt')
                    # Transcribe the file
                    transcription = whisper(str(short_path))
                    transcribe_path.write_text(transcription, encoding='utf-8')
                                        
                    if debug:
                        print(f"{file_name}-{transcription}")    
                    # If the transcription contains the stop word, set the flag
                    if self.stop_word in transcription.lower():
                        stop_threads = True
                        if debug:
                            print(">>>Stopped")
                        break

    def transcribe_whole(self):
        """Perform final transcribe, removing text after stopword."""
        whole_path = Path(self.whole_folder, "whole" + self.file_ext)
        transcription = whisper(str(whole_path))
        transcription = transcription.split(self.stop_word, 1)[0]
        transcription = transcription.split(self.stop_word.proper(), 1)[0]
        return transcription


    def clear_data(self):
        # clear input and output folders
        try:
            shutil.rmtree(self.whole_folder)
            shutil.rmtree(self.short_folder)
            shutil.rmtree(self.transcript_folder)
        except:
            pass
        self.whole_folder.mkdir()
        self.short_folder.mkdir()
        self.transcript_folder.mkdir()

    def start_detection(self):
        # start threads
        threads = []
        threads.append(threading.Thread(target=self.whole_recording))
        threads.append(threading.Thread(target=self.short_recording))
        threads.append(threading.Thread(target=self.transcribe_and_detect_stop))
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def simple_record(self):
        """Used for confirmations."""
        file_name = Path(self.whole_folder, "confirm" + self.file_ext)
        recorder = bluetooth(str(file_name))
        recorder.record()
        time.sleep(self.simple_wait)
        recorder.stop()
        recorder.release()
        
        transcription = whisper(str(file_path)).lower()
        return transcription
