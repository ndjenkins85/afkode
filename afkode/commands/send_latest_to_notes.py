# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""The user wants to send their latest voice transcription to apple notes
"""

import urllib.parse
import webbrowser
from datetime import datetime as dt
from pathlib import Path

from afkode import utils


def execute(not_used) -> str:
    latest_path = sorted([x for x in Path(utils.get_base_path(), "data", "user_response").glob("*.txt")])[-1]

    encoded_text = urllib.parse.quote(latest_path.read_text(encoding="utf-8"))

    shortcut_name = "CreateNote"
    url = f"shortcuts://run-shortcut?name={shortcut_name}&input={encoded_text}"
    webbrowser.open(url)

    response = "saved latest to apple notes"
    return response
