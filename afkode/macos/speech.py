# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains functions related to text-to-speech on MacOS."""

import logging
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue
from typing import List

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from afkode import utils


def text_to_speech(sentence: str, idx: int) -> str:
    """Create a gTTS object.

    Args:
        sentence: input text to be spoken
        idx: index, to increment filename

    Returns:
        Saves a filename for further playing
    """
    logging.info(f">>>{sentence}")
    tts = gTTS(text=sentence, lang="en", tld="com.au")

    # Save the speech audio into a file
    file_name = f"data/text_to_speech/speech_{str(idx).zfill(4)}.mp3"
    tts.save(file_name)
    return file_name


def play_audio(q: Queue) -> None:
    """Play audio files in the queue.

    Args:
        q: Queue for getting through speech.
    """
    played_files = set()

    while True:
        # Wait for a file to become available
        file_name = q.get()

        # Check for the sentinel value that indicates we're done
        if file_name is None:
            q.task_done()
            break

        # Play the audio file
        audio = AudioSegment.from_file(file_name)
        play(audio)

        # Add to the set of played files
        played_files.add(file_name)

        # Mark the task as done
        q.task_done()


def make_dir() -> None:
    """Clear and setup the output directories."""
    target = Path(utils.get_base_path(), "data", "text_to_speech")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)


def split_text(text: str) -> List[str]:
    """Split the given text into sentences.

    Args:
        text: text to be split into different spoken sections.

    Returns:
        List to split text into sections for speech engine.
    """
    # This regular expression matches either a full stop followed by a space or a new line.
    splits = re.split(r"\. |\n|\.\n", text)

    # The filter() function is used to remove empty strings.
    # In Python, empty strings are "falsy" and will be removed by filter.
    splits = list(filter(None, splits))

    return splits


def speak(text: str) -> None:
    """Run text-to-speech on non-ios platform.

    Args:
        text: full text to be spoken.
    """
    make_dir()
    sentences = split_text(text)
    q: Queue = Queue()

    # Start the thread that will play the audio files
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(play_audio, q)

        # Convert each sentence to speech and put the resulting files in the queue
        for i, sentence in enumerate(sentences):
            file_name = text_to_speech(sentence, i)
            q.put(file_name)

        # Signal that we're done
        q.put(None)

    # Wait for all the audio files to be played
    q.join()


def play_blip() -> None:
    """Play a short sound to help notify of API speed."""
    file_name = Path("afkode", "macos", "blip.wav")
    audio = AudioSegment.from_file(file_name)
    play(audio)


if __name__ == "__main__":
    # Can run this module directly for basic speech testing
    utils.setup_logging(log_level=logging.INFO)
    speak("This is a test of the speech module")
