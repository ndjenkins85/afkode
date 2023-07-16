# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

import logging
from datetime import datetime as dt
from pathlib import Path

from afkode import api, utils


def execute(transcript: str) -> str:
    """The user wants to use an AI program to summarize a text input into a few short words, for use in a filename.

    Args:
        transcript: transcription input from user

    Returns:
        Chatgpt response, limited to four words
    """
    prompt = Path(utils.get_prompt_path(), "programflow", "proposed_filename.txt").read_text(encoding="utf-8")
    request = prompt + "\n\n--------- Here is the user input:\n" + transcript

    logging.debug(request)
    response = api.chatgpt(request)

    proposed_filename = " ".join(f"{response}    ".split(" ")[:4]).strip()
    output_path = Path(utils.get_user_prompt_directory(), f"{dt.now()} - {proposed_filename}.txt")
    output_path.write_text(transcript, encoding="utf-8")
    return proposed_filename
