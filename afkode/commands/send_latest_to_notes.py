# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

import urllib.parse
import webbrowser
from pathlib import Path

from afkode import utils


def execute(not_used: str) -> str:
    """The user wants to send their latest voice transcription to apple notes.

    Args:
        not_used: not_used for consistency

    Returns:
        confirmation
    """
    latest_path = sorted([x for x in Path(utils.get_base_path(), "data", "user_response").glob("*.txt")])[-1]

    encoded_text = urllib.parse.quote(latest_path.read_text(encoding="utf-8"))

    shortcut_name = "CreateNote"
    url = f"shortcuts://run-shortcut?name={shortcut_name}&input={encoded_text}"
    webbrowser.open(url)

    response = "saved latest to apple notes"
    return response
