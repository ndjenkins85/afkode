# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from afkode import api


def execute(optional_additional_instructions: str) -> str:
    """This file is only a template and doesn't perform any useful actions.

    It is useful to help an AI agent interpret how to create new commands.
    This section is the docstring documentation which describes user intent.

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
