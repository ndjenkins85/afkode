# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from datetime import datetime as dt
from pathlib import Path

from afkode import api, utils


def execute(all_additional_instructions_provided_after_command: str) -> str:
    """The user wants to use an AI program to summarize many different text files in a folder.

    Specifically ones with today's date.

    Args:
        all_additional_instructions_provided_after_command: all_additional_instructions_provided_after_command

    Returns:
        Chatgpt reponse
    """
    today = str(dt.now())[:10]
    todays_files = sorted(
        [x for x in Path(utils.get_base_path(), "data", "user_response").glob("*.txt") if x.name[:10] == today]
    )

    summarize_prompt = """Your task is to summarize the following thoughts from a
    user who is using a voice transcription system"""

    data = ""
    for file in todays_files:
        data += file.read_text(encoding="utf-8") + "\n"

    # Include additional instructions
    request = summarize_prompt + "\n" + all_additional_instructions_provided_after_command + "\n" + data
    response = api.chatgpt(request)

    return response
