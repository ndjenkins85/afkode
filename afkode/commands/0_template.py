# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from afkode import api


def execute(optional_additional_instructions: str) -> str:
    """This file is a template to help create new commands. This section is the file documentation.

    in which it is important to put information about what the command is, and how it helps the user perform tasks

    Args:
        optional_additional_instructions: optional_additional_instructions

    Returns:
        response from chatgpt for speech
    """
    # Create a prompt request
    prompt = "Tell me a story about..."

    # Put together the request
    request = prompt + optional_additional_instructions

    # Send completed data to API and return response
    response = api.chatgpt(request)
    return response
