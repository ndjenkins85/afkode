# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""This file contains functions related to interacting with external API systems."""

import openai

from ai_cookie import (
    secrets,  # We load secrets from a python file to support pythonista
)

openai.api_key = secrets.OPENAI_KEY


def whisper(path: str) -> str:
    """Basic transcription from filepath."""
    transcript = openai.Audio.translate("whisper-1", open(path, "rb"), options={"language": "en", "temperature": "0"})
    return transcript.text


def chatgpt(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Basic ChatGPT prompt only."""
    completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
    raw_commands = completion.choices[0].message.content
    return raw_commands
