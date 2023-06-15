# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file contains functions related to interacting with external API systems."""

import openai

from ai_cookie import (
    secrets,  # We load secrets from a python file to support pythonista
)

openai.api_key = secrets.OPENAI_KEY


def whisper(path: str) -> str:
    """Transcribes audio from the specified file path using the Whisper API.

    Args:
        path: The path to the audio file.

    Returns:
        The transcribed text.
    """
    transcript = openai.Audio.translate("whisper-1", open(path, "rb"), options={"language": "en", "temperature": "0"})
    return transcript.text


def chatgpt(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Sends a prompt to the ChatGPT API for chat-based language generation.

    Args:
        prompt: The prompt text.
        model: The name of the model to use. Default is "gpt-3.5-turbo".

    Returns:
        The generated text response.
    """
    completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
    raw_commands = completion.choices[0].message.content
    return raw_commands
