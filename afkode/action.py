# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This module provides a Command class for recognizing and executing voice commands.

Each command corresponds to a Python file in the 'command' directory with an 'execute' function.
"""
import importlib
import json
import logging
from pathlib import Path

from afkode import api, utils


class Command:
    """Allows for selection of commands from extra folder."""

    def __init__(self, transcript: str) -> None:
        """Initialize the Command with a transcript of the user's voice input.

        Args:
            transcript (str): The transcript of the user's voice input.
        """
        self.transcript = transcript.lower()
        self.command = None
        self.instructions = ""
        self.command_word = "command"
        self._parse_transcript()

    def _parse_transcript(self) -> None:
        """Parse the transcript to recognize a command and its instructions."""
        command_data = utils.split_transcription_on(self.transcript, self.command_word, strategy="after")
        # Will be shorter than original if there was a command word
        if len(command_data) < len(self.transcript):
            self.collate_and_choose_command(command_data)

    def collate_and_choose_command(self, command_candidate: str) -> None:
        """Check the 'command' directory for a file matching the command_candidate.

        Args:
            command_candidate (str): The potential command name to look for.
        """
        options = utils.get_formatted_command_list()

        # Get our command prompt
        choose_command_prompt = Path(utils.get_prompt_path(), "programflow", "choose_command.txt").read_text()

        choose_command_request = (
            choose_command_prompt + "\nUser input:" + command_candidate + f"\n{'-'*20}Options:\n" + options
        )
        choose_command_response = api.chatgpt(choose_command_request)
        logging.debug(f"Request: {choose_command_request}")
        logging.info(f"Command: {choose_command_response}")

        self.command = json.loads(choose_command_response).get("command")
        self.instructions = json.loads(choose_command_response).get("parameters")

    def execute(self) -> str:
        """Execute the recognized command by importing its module and calling its 'execute' function.

        Returns:
            str: The result of the 'execute' function if the command was recognized, otherwise None.

        Raises:
            ImportError: If the command was not recognized.
        """
        if self.command:
            try:
                module = importlib.import_module(f"afkode.commands.{self.command}")
                return module.execute(self.instructions)
            except ImportError:
                logging.warning(f"Tried to import a non-existant command {self.command}")

        return "No command"
