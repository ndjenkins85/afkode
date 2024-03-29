# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""
from afkode import utils


def execute(all_additional_instructions_provided_after_command: str) -> str:
    """The user wants information from a file system about what command names are available.

    Args:
        all_additional_instructions_provided_after_command: all_additional_instructions_provided_after_command

    Returns:
        list of commands
    """
    command_files = utils.get_spoken_command_list()
    response = "List of commands: " + "\n".join(command_files)
    return response
