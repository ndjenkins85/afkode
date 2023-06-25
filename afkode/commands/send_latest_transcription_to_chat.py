# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from datetime import datetime as dt
from pathlib import Path

from afkode import api, utils


def execute(not_used: str) -> str:
    """The user wants to send their latest voice transcription saved file to a chatbot.

    Args:
        not_used: not_used

    Returns:
        response from chatgpt
    """
    latest_path = sorted(Path(utils.get_user_prompt_directory()).glob("*.txt"))[-1]

    request = latest_path.read_text(encoding="utf-8")
    response = api.chatgpt(request)

    output_path = Path(utils.get_agent_response_directory(), f"{dt.now()}.txt")
    output_path.write_text(response, encoding="utf-8")

    return response
