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
    def __init__(self, transcript):
        """Initialize the Command with a transcript of the user's voice input.

        Args:
            transcript (str): The transcript of the user's voice input.
        """
        self.transcript = transcript.lower()
        self.command = None
        self.instructions = None

        self._parse_transcript()

    def _parse_transcript(self):
        """Parse the transcript to recognize a command and its instructions."""
        words = self.transcript.split("command")
        if len(words) > 1:
            # get last info after command
            self.collate_and_choose_command(words[-1])

    def collate_and_choose_command(self, command_candidate):
        """Check the 'command' directory for a file matching the command_candidate.

        Args:
            command_candidate (str): The potential command name to look for.
        """
        command_dir = Path(utils.get_base_path(), "afkode", "commands")
        ignore = ["__init__"]
        command_files = [f.stem for f in command_dir.glob("*.py") if f.stem not in ignore]

        # Get all commands ready for a prompt
        options = ""
        for command_file in command_files:
            options += command_file + "\n"
            command_data = Path(command_dir, f"{command_file}.py").read_text(encoding="utf-8")
            drop = "# -*- coding: utf-8 -*-\n# Copyright © 2023 by Nick Jenkins. All rights reserved"
            command_data = command_data.replace(drop, "")
            # Ignore the code after the docstrings and definition, as it may contain prompt info
            command_data = command_data.split(") -> str:")[0]
            options += command_data + "\n\n"

        # Get our command prompt
        choose_command_prompt = Path(get_base_path(), "prompts", "programflow", "choose_command.txt").read_text()

        choose_command_request = (
            choose_command_prompt + "\nUser input:" + command_candidate + f"\n{'-'*20}Options:\n" + options
        )
        choose_command_response = api.chatgpt(choose_command_request, model="gpt-3.5-turbo-16k")
        logging.debug(f"Request: {choose_command_request}")
        logging.info(f"Command: {choose_command_response}")

        self.command = json.loads(choose_command_response).get("command")
        self.instructions = json.loads(choose_command_response).get("parameters")

    def execute(self):
        """
        Execute the recognized command by importing its module and calling its 'execute' function.

        Returns:
            The result of the 'execute' function if the command was recognized, otherwise None.

        Raises:
            ValueError: If the command was not recognized.
        """
        if self.command:
            try:
                module = importlib.import_module(f"afkode.commands.{self.command}")
                return module.execute(self.instructions)
            except ImportError:
                logging.warning(f"Tried to import a non-existant command {self.command}")
        return None
