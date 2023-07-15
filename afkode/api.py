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
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from afkode import utils


def get_credentials() -> Dict[str, str]:
    """Loads credentials for API calls.

    Returns:
        Credentials from several services used in API calls
    """
    credentials = {"GOOGLE_SERVICE_ACCOUNT": "", "OPENAI_KEY": "", "GOOGLE_KEY": "", "GOOGLE_OATH2": ""}

    google_service_credentials_path = Path(utils.get_base_path(), "credentials", "google.json")
    if google_service_credentials_path.exists():
        credentials["GOOGLE_SERVICE_ACCOUNT"] = json.loads(google_service_credentials_path.read_text())
    elif os.getenv("GOOGLE_SERVICE_ACCOUNT"):
        google_service_account = str(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
        credentials["GOOGLE_SERVICE_ACCOUNT"] = json.loads(google_service_account)

    api_keys_path = Path(utils.get_base_path(), "credentials", "api_keys.json")
    if api_keys_path.exists():
        credentials["OPENAI_KEY"] = json.loads(api_keys_path.read_text()).get("OPENAI_KEY")
        credentials["GOOGLE_KEY"] = json.loads(api_keys_path.read_text()).get("GOOGLE_KEY")
    else:
        credentials["OPENAI_KEY"] = os.getenv("OPENAI_KEY", "")
        credentials["GOOGLE_KEY"] = os.getenv("GOOGLE_KEY", "")

    if credentials.get("GOOGLE_SERVICE_ACCOUNT"):
        gsa_credentials = service_account.Credentials.from_service_account_file(google_service_credentials_path)
        scoped_credentials = gsa_credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])
        # Refresh the credentials
        if not scoped_credentials.valid:
            scoped_credentials.refresh(Request())
        credentials["GOOGLE_OATH2"] = scoped_credentials.token
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
            "whisper-1",
            open(path, "rb"),
            options={
                "language": "en",
                "temperature": "0",
                "beam_size": 3,
                "compression_ratio_threshold": 2.4,
                "condition_on_previous_text": False,
            },
        ).text
    except openai.error.InvalidRequestError:
        logging.error("Whisper API received <0.1s audio file")
        transcript = ""
    except openai.error.APIConnectionError:
        logging.error("Whisper API connection error")
        # speak("Connection error")
        transcript = "exit"

    # Whisper is prone to hallucinations, so we suppress known hallucination outputs
    # They aren't really a problem at least in the longer transcripts, but they mess up the logging
    hallucinations_path = Path(utils.get_base_path(), "afkode", "prompts", "debug", "whisper_hallucinations.txt")
    hallucinations = hallucinations_path.read_text().split("\n")
    if transcript in hallucinations:
        logging.debug("Hallucination detected")
        transcript = ""

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
        # speak("Connection error")
        raw_commands = "exit"
    return raw_commands


def google_tts(output_path: Path, text_input: str = None, ssml_input: str = None) -> None:
    """Converts text to speech audio file and saves.

    Args:
        output_path: Location to write completed google TTS file
        text_input: Text input for text to speech
        ssml_input: Alternatively pass in SSML input for text to speech
    """
    # Define the endpoint URL
    url = f'https://texttospeech.googleapis.com/v1/text:synthesize?key={get_credentials()["GOOGLE_KEY"]}'
    headers = {
        "Authorization": f'Bearer {get_credentials()["GOOGLE_OATH2"]}',
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "effectsProfileId": ["small-bluetooth-speaker-class-device"],
            "pitch": 2,
            "speakingRate": 1.1,
        },
        "input": {"text": text_input, "ssml": ssml_input},
        "voice": {"name": "en-AU-Polyglot-1", "languageCode": "en-AU"},
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)

    # Print the response
    if response.status_code == 200:
        # Decode the base64 string
        byte_data = base64.b64decode(response.json().get("audioContent"))
        logging.info(f"Writing audio file to {output_path}")
        with open(output_path, "wb") as f:
            f.write(byte_data)
    else:
        logging.error(f"Invalid status code {response.status_code}")
