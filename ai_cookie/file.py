# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""This module is responsible for detecting file commands."""

import logging
from pathlib import Path

from ai_cookie import utils


class FileIO:
    def __init__(self):
        self.confirm_words = ["yes", "yeah", "ok", "affirmative", "acknowledged"]
        self.commands_destructive = ["save", "make"]
        self.commands_harmless = ["load", "list", "change", "where"]
        self.pending_command = []
        self.cwd = Path("..")
        self.latest_response = None

    def command(self, transcription: str) -> str:
        transcript = transcription.lower().split()
        if transcript[0] == "exit":
            return "exit"
        elif transcript[0] != "command":
            return ""
        elif transcript[1] in self.commands_destructive:
            self.pending_command = transcript[1:3]
            return "confirm"
        elif transcript[1] in self.commands_harmless:
            self.execute_command(transcript[1], transcript[2])

    def confirm(self, transcription: str) -> bool:
        for affirm in self.confirm_words:
            if affirm in transcription:
                self.execute_command(*self.pending_command)
                return True
        return False

    def execute_command(self, command, variable):
        self.pending_command = None
        if command == "save":
            save_file = Path(self.cwd, variable + ".txt")
            save_file.write_text(self.latest_response)
            return f"Saved {variable}"
        if command == "make":
            Path(self.cwd, variable).mkdir()
            return f"Created folder {variable}"
        if command == "load":
            load_file = Path(self.cwd, variable + ".txt")
            if load_file.exists():
                self.latest_response = load_file.read_text()
                return f"Loaded {variable}"
            else:
                return f"Load failed, {variable} does not exist"
        if command == "list":
            files = list(self.cwd.iterdir())
            return "Folder contents: " + ",".join(files)
        if command == "change":
            if variable == "up":
                self.cwd = Path(self.cwd, "..")
                return str(f"Current working directory: {self.cwd}")
            elif Path(self.cwd, variable).is_folder():
                self.cwd = Path(self.cwd, variable)
                return str(f"Current working directory: {self.cwd}")
            else:
                return str(f"No such folder {variable}")
        if command == "where":
            return str(f"Current working directory: {self.cwd}")

    def save_response(self, transcript: str, file_name: str) -> None:
        """Save file to the user response section."""
        output_path = Path(utils.get_user_prompt_directory(), file_name.lower().strip() + ".txt")
        logging.info(f">>>Saving to {output_path}")
        output_path.write_text(transcript, encoding="utf-8")
