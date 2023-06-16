# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""The user wants information from a file system about what command names are available
"""

from datetime import datetime as dt
from pathlib import Path

from ai_cookie import api


def execute(all_additional_instructions_provided_after_command) -> str:
    command_dir = Path("ai_cookie", "commands")
    ignore = ["__init__"]
    command_files = [f.stem for f in command_dir.glob("*.py") if f.stem not in ignore]

    response = "List of commands: " + "\n".join(command_files.replace("_", " "))
    return response
