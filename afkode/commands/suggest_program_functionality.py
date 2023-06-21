# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from pathlib import Path

from afkode import api, meta, utils


def execute(not_used: str) -> str:
    """The user seeks a review of the codebase to see what additional functionality should be added.

    Args:
        not_used: not_used

    Returns:
        Chatgpt reponse
    """
    program_commands_prompt = Path(utils.get_prompt_path(), "debug", "program_functionality.txt").read_text()

    readme = meta.get_formatted_readme()

    file_data = ""
    input_files = utils.resolve_input_paths(["/**/*.py"], exclude=["__init__.py"])
    for input_file in input_files:
        clean = meta.clean_py(input_file.read_text(encoding="utf-8"))
        file_data += f"File: {str(input_file)} ****\n"
        file_data += clean + "\n\n"

    request = program_commands_prompt + "\n\n" + readme + "\n\n" + file_data
    response = api.chatgpt(request, "gpt-3.5-turbo-16k")
    return response
