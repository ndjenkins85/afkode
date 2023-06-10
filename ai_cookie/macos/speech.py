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
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def text_to_speech(sentence, idx):
    # Create a gTTS object
    tts = gTTS(text=sentence, lang="en", tld="com.au")

    # Save the speech audio into a file
    file_name = f"data/text_to_speech/speech_{str(idx).zfill(4)}.mp3"
    tts.save(file_name)

    return file_name


def play_audio(q):
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
    target = Path("data/text_to_speech")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()


def split_text(text):
    # This regular expression matches either a full stop followed by a space or a new line.
    splits = re.split("\. |\n|\.\n", text)

    # The filter() function is used to remove empty strings.
    # In Python, empty strings are "falsy" and will be removed by filter.
    splits = list(filter(None, splits))

    return splits


def speak(text) -> None:
    """Run text-to-speech on non-ios platform."""
    make_dir()
    sentences = split_text(text)
    q = Queue()

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
