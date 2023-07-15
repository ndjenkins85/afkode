# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Main controller for voice recording and stop detection."""

import logging
import queue
import shutil
import threading
import time
import wave
from pathlib import Path

# Any script entry must have this
# For it to work on pythonista
try:
    import set_env  # noqa: F401

    from afkode.ios.listen import bluetooth
    from afkode.ios.speech import play_blip
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401
    from afkode.macos.listen import bluetooth
    from afkode.macos.speech import play_blip

from afkode import api, globals, utils


class VoiceRecorder:
    """Main controller for voice recording and stop deteection."""

    def __init__(self) -> None:
        """Initialize the VoiceRecorder."""
        self.folder_base = Path(utils.get_base_path(), "data", "detect_stop")
        if not self.folder_base.exists():
            self.folder_base.mkdir(parents=True)

        self.whole_folder = Path(self.folder_base, "whole")
        self.short_folder = Path(self.folder_base, "short")
        self.start_folder = Path(self.folder_base, "start")
        self.transcript_folder = Path(self.folder_base, "transcript")
        self.file_ext = ".wav"
        self.simple_wait = 3
        self.load_config()

    def load_config(self) -> None:
        """Load relevant configuration options."""
        config = utils.load_config()
        self.short_time = config.get("short_time", 3)
        self.tick = config.get("tick", 0.1)
        self.start_word = config.get("start_word", "")
        self.stop_word = config.get("stop_word", "")
        self.size_threshold_bytes = config.get("size_threshold_bytes", 10 * 1024)
        self.max_record_seconds = config.get("max_record_seconds", 420)

    def short_recording(self, q) -> None:  # type: ignore # noqa: ANN001
        """We use shorter recordings for stop word detection every few seconds.

        Args:
            q: Queue to hold completed audio paths.
        """
        file_counter = 1
        while not globals.stop_threads:
            short_audio_path = Path(self.short_folder, "short" + str(file_counter).zfill(4) + self.file_ext)
            recorder = bluetooth(str(short_audio_path))
            recorder.record()
            for _ in range(int(self.short_time / self.tick)):
                time.sleep(self.tick)
                if globals.stop_threads:
                    break
            recorder.stop()
            recorder.release()
            file_counter += 1

            # Maximum record time
            if (file_counter * self.short_time) > self.max_record_seconds:
                logging.info(f"Reached maximum record time {self.max_record_seconds}")
                globals.stop_threads = True

            # Fallback in case for some reason the recorder is failing to produce proper files
            if short_audio_path.stat().st_size >= self.size_threshold_bytes:
                q.put(short_audio_path)
            else:
                logging.warning(f"Invalid file size for {short_audio_path.name}, recording not working?")

    def transcribe_and_detect_stop(self, q) -> None:  # type: ignore # noqa: ANN001
        """Transcribe short recordings and detect stop words.

        Args:
            q: Queue to hold completed audio paths.
        """
        while not globals.stop_threads:
            short_audio_path = q.get()
            transcribe_path = Path(self.transcript_folder, f"{short_audio_path.name}.txt")

            # Transcribe the file
            transcription = api.whisper(str(short_audio_path))
            transcribe_path.write_text(transcription, encoding="utf-8")
            play_blip()

            logging.info(f"{short_audio_path.stem} <<< {transcription}")

            # Will be shorter than original if there was a start word
            start_test = utils.split_transcription_on(transcription, words=self.start_word, strategy="detect")
            if len(start_test.strip()) < len(transcription.strip()):
                Path(self.start_folder, f"{short_audio_path.name}.txt").touch()
                logging.info("<<<Start command")

            # Will be shorter than original if there was a start word
            stop_test = utils.split_transcription_on(transcription, words=self.stop_word, strategy="detect")
            if len(stop_test.strip()) < len(transcription.strip()):
                # If stop word, set the break flag leading to stopping recording
                globals.stop_threads = True
                logging.debug("Transcribe stopped")
                q.task_done()
                break
            q.task_done()

    def transcribe_whole(self) -> str:
        """Perform final transcribe, removing text after stopword.

        Returns:
            Transcribed text
        """
        whole_path = Path(self.whole_folder, "whole" + self.file_ext)
        transcription = api.whisper(str(whole_path))

        transcription = utils.split_transcription_on(transcription, words=self.start_word, strategy="after")
        transcription = utils.split_transcription_on(transcription, words=self.stop_word, strategy="before")

        whole_output_path = Path(self.whole_folder, "whole.txt")
        whole_output_path.write_text(transcription, encoding="utf-8")
        return transcription

    def clear_data(self) -> None:
        """Clear input and output folders."""
        try:
            shutil.rmtree(self.whole_folder)
            shutil.rmtree(self.short_folder)
            shutil.rmtree(self.transcript_folder)
            shutil.rmtree(self.start_folder)
        except Exception:
            logging.info("No folder removal needed")
        self.whole_folder.mkdir()
        self.short_folder.mkdir()
        self.transcript_folder.mkdir()
        self.start_folder.mkdir()

    def start_detection(self) -> None:
        """Start the voice detection process."""
        globals.stop_threads = False
        q = queue.Queue()  # type: ignore
        t1 = threading.Thread(target=self.short_recording, args=(q,))
        t2 = threading.Thread(target=self.transcribe_and_detect_stop, args=(q,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.combine_wav_files()

    def simple_record(self) -> str:
        """Used for confirmations.

        Returns:
            Transcription of recorded text
        """
        file_name = Path(self.whole_folder, "confirm" + self.file_ext)
        recorder = bluetooth(str(file_name))
        recorder.record()
        time.sleep(self.simple_wait)
        recorder.stop()
        recorder.release()

        transcription = api.whisper(str(file_name)).lower()
        return transcription

    def combine_wav_files(self) -> None:
        """Combines several .wav files into a single one for transcription."""
        # Get all transcribed data (smaller than all 'recorded')
        all_transcripts = sorted(self.transcript_folder.glob("*.wav.txt"))

        # Find the latest ever reset, but include the first as a minimum if no reset
        Path(self.start_folder, "short0001.wav.txt").touch()
        latest_restart = sorted(self.start_folder.glob("*.wav.txt"))[-1].name

        # Get minimum set of short .wav files based on valid transcript files
        min_transcripts = [x for x in all_transcripts if x.name >= latest_restart]
        min_shorts = sorted([Path(self.short_folder, file.name.replace(".txt", "")) for file in min_transcripts])

        # Populate the larger .wav file with min set of short audio .wav files
        output_filename = Path(self.whole_folder, "whole" + self.file_ext)
        with wave.open(str(output_filename), "wb") as output_wav:
            for i, short_audio_path in enumerate(min_shorts):
                logging.debug(f"Stitching {short_audio_path}")
                with wave.open(str(short_audio_path), "rb") as input_wav:
                    # If this is the first file, set output parameters
                    if i == 0:
                        output_wav.setparams(input_wav.getparams())
                    output_wav.writeframes(input_wav.readframes(input_wav.getnframes()))
