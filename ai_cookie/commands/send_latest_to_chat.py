# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""The user wants to send their latest voice transcription saved file to a chatbot.
"""

from datetime import datetime as dt
from pathlib import Path

from ai_cookie import api


def execute(all_additional_instructions_provided_after_command) -> str:
    latest_path = sorted([x for x in Path("data", "user_response").glob("*.txt")])[-1]

    latest = latest_path.read_text(encoding="utf-8")

    # Include additional instructions
    request = latest + "\n" + all_additional_instructions_provided_after_command
    response = api.chatgpt(request)

    return response
