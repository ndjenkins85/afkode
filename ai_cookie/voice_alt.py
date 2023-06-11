# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

import logging
import os
import shutil
import threading
import time
import wave
from pathlib import Path

from ai_cookie import utils

if utils.running_on_pythonista():
    from ai_cookie.ios.listen import bluetooth
else:
    from ai_cookie.macos.listen import bluetooth

from ai_cookie.api import chatgpt, whisper
from ai_cookie.globals import *


class VoiceRecorder:
    def __init__(self):
        self.folder_base = Path("data", "detect_stop")
        if not self.folder_base.exists():
            self.folder_base.mkdir()

        self.whole_folder = Path(self.folder_base, "whole")
        self.short_folder = Path(self.folder_base, "short")
        self.transcript_folder = Path(self.folder_base, "transcript")
        self.file_ext = ".wav"
        self.short_time = 3
        self.simple_wait = 3
        self.tick = 1
        self.stop_word = " stop"

    def short_recording(self):
        """We use shorter recordings for stop word detection every few seconds."""
        global stop_threads
        time.sleep(1)  # Add a slight delay for the recording
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
        while not stop_threads:
            # Get the list of input files and output files, ignoring latest partial recording
            time.sleep(self.short_time - self.tick)
            input_files = sorted(os.listdir(self.short_folder))[:-1]
            output_files = os.listdir(self.transcript_folder)

            # Check each input file
            for file_name in input_files:
                # If this file hasn't been transcribed yet
                if f"{file_name}.txt" not in output_files:
                    short_path = Path(self.short_folder, file_name)
                    transcribe_path = Path(self.transcript_folder, f"{file_name}.txt")
                    # Transcribe the file
                    transcription = whisper(str(short_path))
                    transcribe_path.write_text(transcription, encoding="utf-8")

                    logging.info(f"{file_name} <<< {transcription}")
                    # If the transcription contains the stop word, set the flag
                    if self.stop_word in " " + transcription.lower():
                        stop_threads = True
                        logging.debug("Transcribe stopped")
                        break

    def transcribe_whole(self):
        """Perform final transcribe, removing text after stopword."""
        time.sleep(0.5)
        whole_path = Path(self.whole_folder, "whole" + self.file_ext)
        transcription = whisper(str(whole_path))
        transcription = transcription.split(self.stop_word, 1)[0]
        transcription = transcription.split(self.stop_word.title(), 1)[0]
        whole_output_path = Path(self.whole_folder, "whole.txt")
        whole_output_path.write_text(transcription, encoding="utf-8")
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
        global stop_threads
        stop_threads = False
        # start threads
        threads = []
        threads.append(threading.Thread(target=self.short_recording))
        threads.append(threading.Thread(target=self.transcribe_and_detect_stop))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.combine_wav_files()

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

    def combine_wav_files(self):
        output_filename = Path(self.whole_folder, "whole" + self.file_ext)
        combine_audio_list = sorted(list(Path("data", "detect_stop", "transcript").iterdir()))
        combine_audio_list = [str(x).replace("/transcript/", "/short/").replace(".txt", "") for x in combine_audio_list]

        with wave.open(str(output_filename), "wb") as output_wav:
            # Process each input file
            for wav_file in combine_audio_list:
                logging.debug(f"Stitching {wav_file}")
                with wave.open(str(wav_file), "rb") as input_wav:
                    # If this is the first file, set output parameters
                    if output_wav.getnframes() == 0:
                        output_wav.setparams(input_wav.getparams())

                    # Write frames to output file
                    output_wav.writeframes(input_wav.readframes(input_wav.getnframes()))
