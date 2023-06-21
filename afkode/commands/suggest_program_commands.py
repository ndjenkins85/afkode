# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from datetime import datetime as dt
from pathlib import Path

from afkode import api, meta, utils


def execute(not_used: str) -> str:
    """The user seeks a review of the codebase and the available commands, to receive suggestions of new command functionality.

    Args:
        not_used: not_used

    Returns:
        Chatgpt reponse
    """
    program_commands_prompt = Path(utils.get_prompt_path(), "debug", "program_commands.txt").read_text()

    readme = meta.get_formatted_readme()
    run = utils.clean_py(Path(utils.get_base_path(), "afkode", "run.py").read_text(encoding="utf-8"))
    commands = utils.get_formatted_command_list()

    request = program_commands_prompt + "\n\n" + readme + "\n\n" + run + "\n\n" + commands
    response = api.chatgpt(request)
    return response
