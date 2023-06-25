# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

import urllib.parse
import webbrowser
from pathlib import Path

from afkode import utils


def execute(not_used: str) -> str:
    """The user wants to send the latest reponse from an AI agent to their apple notes.

    Args:
        not_used: not_used for consistency

    Returns:
        confirmation
    """
    latest_path = sorted(Path(utils.get_agent_response_directory()).glob("*.txt"))[-1]

    title = latest_path.name[:10] + " agent response"
    encoded_text = latest_path.read_text(encoding="utf-8")
    data = urllib.parse.quote(title + "\n\n" + encoded_text)

    shortcut_name = "CreateNote"
    url = f"shortcuts://run-shortcut?name={shortcut_name}&input={data}"
    webbrowser.open(url)

    response = "Saved"
    return response
