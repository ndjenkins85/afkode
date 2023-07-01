# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file contains functions related to interacting with external API systems."""

import base64
import json
import logging
import os
from pathlib import Path
from typing import Dict

import openai
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from afkode import utils

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env  # noqa: F401

    from afkode.ios.speech import speak
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401
    from afkode.macos.speech import speak


def get_credentials() -> Dict[str, str]:
    """Loads credentials for API calls."""
    credentials = {
        "GOOGLE_SERVICE_ACCOUNT": None,
        "OPENAI_KEY": None,
        "GOOGLE_KEY": None,
    }
    google_service_credentials_path = Path(utils.get_base_path(), "credentials", "google.json")
    if google_service_credentials_path.exist():
        credentials["GOOGLE_SERVICE_ACCOUNT"] = json.loads(google_service_credentials_path.read_text())
    else:
        credentials["GOOGLE_SERVICE_ACCOUNT"] = json.loads(os.getenv("OPENAI_KEY"))

    api_keys_path = Path(utils.get_base_path(), "credentials", "api_keys.json")
    if api_keys_path.exists():
        credentials["OPENAI_KEY"] = json.loads(api_keys_path.read_text()).get("OPENAI_KEY")
        credentials["GOOGLE_KEY"] = json.loads(api_keys_path.read_text()).get("GOOGLE_KEY")
    else:
        credentials["OPENAI_KEY"] = os.getenv("OPENAI_KEY")
        credentials["GOOGLE_KEY"] = os.getenv("GOOGLE_KEY")
    return credentials


def whisper(path: str) -> str:
    """Transcribes audio from the specified file path using the Whisper API.

    Args:
        path: The path to the audio file.

    Returns:
        The transcribed text.
    """
    openai.api_key = get_credentials()["OPENAI_KEY"]
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
    openai.api_key = get_credentials()["OPENAI_KEY"]
    try:
        completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
        raw_commands = completion.choices[0].message.content
    except openai.error.APIConnectionError:
        logging.error("Whisper API connection error")
        speak("Connection error")
        raw_commands = "exit"
    return raw_commands
