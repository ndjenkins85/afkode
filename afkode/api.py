# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file contains functions related to interacting with external API systems."""

import os

import openai

# We load secrets from a python file to support pythonista
try:
    from afkode import secrets  # type: ignore

    openai.api_key = secrets.OPENAI_KEY
except ImportError:
    try:
        openai.api_key = os.getenv("OPENAI_KEY")
    except NameError as name_err:
        raise ValueError(
            """You need to set an environment variable 'OPENAI_KEY'
            export OPENAI_KEY=sk-
            """
        ) from name_err

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env  # noqa: F401

    from afkode.ios.speech import speak
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401
    from afkode.macos.speech import speak


def whisper(path: str) -> str:
    """Transcribes audio from the specified file path using the Whisper API.

    Args:
        path: The path to the audio file.

    Returns:
        The transcribed text.
    """
    try:
        transcript = openai.Audio.translate(
            "whisper-1", open(path, "rb"), options={"language": "en", "temperature": "0"}
        ).text
    except openai.error.InvalidRequestError:
        logging.error("Whisper API received <0.1s audio file")
        transcript = ""
    except openai.error.APIConnectionError:
        logging.error("Whisper API connection error")
        speak("Connection error")
        transcript = "exit"
    return transcript


def chatgpt(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Sends a prompt to the ChatGPT API for chat-based language generation.

    Args:
        prompt: The prompt text.
        model: The name of the model to use. Default is "gpt-3.5-turbo".

    Returns:
        The generated text response.
    """
    try:
        completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
        raw_commands = completion.choices[0].message.content
    except openai.error.APIConnectionError:
        logging.error("Whisper API connection error")
        speak("Connection error")
        raw_commands = "exit"
    return raw_commands
