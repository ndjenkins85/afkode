# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""The user wants to send their latest voice transcription saved file to a chatbot.
"""

from datetime import datetime as dt
from pathlib import Path

from afkode import api


def execute(not_used) -> str:
    latest_path = sorted([x for x in Path("data", "user_response").glob("*.txt")])[-1]

    request = latest_path.read_text(encoding="utf-8")
    response = api.chatgpt(request)

    return response
