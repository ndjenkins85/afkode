# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains functions related to recording speech on MacOS."""

import logging
import threading
import time
import wave
from pathlib import Path
from typing import List

import pyaudio

from afkode import utils


class Recorder:
    """MacOS specific audio recording."""

    def __init__(self, file_name: str, chunk: int = 1024, channels: int = 1, rate: int = 44100) -> None:
        """Initialize Recorder object.

        Args:
            file_name: Name of the output file.
            chunk: Number of audio frames per buffer.
            channels: Number of audio channels.
            rate: Sample rate of the audio.
        """
        self.file_name = file_name
        self.chunk = chunk
        self.channels = channels
        self.rate = rate

        self.audio = pyaudio.PyAudio()
        self.frames: List[bytes] = []
        self.recording = False

    def record(self) -> None:
        """Start recording audio."""
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self) -> None:
        """Stop recording audio."""
        self.recording = False
        self.thread.join()

    def _record(self) -> None:
        """Internal method for audio recording."""
        stream = self.audio.open(
            format=pyaudio.paInt16, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk
        )

        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

    def release(self) -> None:
        """Release recorded audio and save to file."""
        wf = wave.open(self.file_name, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frames))
        wf.close()


def bluetooth(file_name: str) -> Recorder:
    """Example usage: Obtain a Recorder object using a Bluetooth connection.

    Args:
        file_name: Name of the output file.

    Returns:
        Recorder object.
    """
    return Recorder(file_name)


def basic_record(file_name: str, record_time: int) -> None:
    """Record audio for a specified duration.

    Args:
        file_name: Name of the output file.
        record_time: Duration of the recording in seconds.
    """
    recorder = bluetooth(file_name)
    recorder.record()
    time.sleep(record_time)
    recorder.stop()
    recorder.release()


if __name__ == "__main__":
    # Can run this module directly for basic recording testing
    utils.setup_logging(log_level=logging.INFO)
    logging.info("Recording for 5 seconds")
    output_file_path = Path("data", "detect_stop", "basic_record_test.wav")
    basic_record(str(output_file_path), 5)
    logging.info(f"Saved recording to {output_file_path}")
