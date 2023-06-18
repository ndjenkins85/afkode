# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains utility functions used throughout the AFKode project."""

import logging
import re
import time
from pathlib import Path

from afkode.globals import *


def setup_logging(log_level=logging.DEBUG) -> None:
    """Configures the logging settings for the application.

    Args:
        log_level: The log level to set. Default is DEBUG.
    """
    log_path = Path("logs", "_log.txt")
    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f'''Directory {log_path} missing, cannot create log file.
                  Make sure you are running from base of repo, with correct data folder structure.
                  Continuing without log file writing.'''
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)


def running_on_pythonista() -> bool:
    """Checks if the program is running on iOS (pythonista) or MacOS (poetry-python).

    Returns:
        True if running on iOS, False if running on MacOS.
    """
    try:
        import console

        logging.info("Running on iOS (pythonista)")
        return True
    except ModuleNotFoundError:
        logging.info("Running on MacOS (poetry-python)")
        return False


def get_user_prompt_directory() -> Path:
    """Retrieves the directory path for user input.

    Returns:
        The path to the user input directory.
    """
    user_prompt_directory_path = Path("data", "user_response")
    if not user_prompt_directory_path.exists():
        user_prompt_directory_path.mkdir()
    return user_prompt_directory_path


def get_user_prompt_files() -> str:
    """Retrieves a string of all the filenames in the user input directory.

    Returns:
        The string of filenames.
    """
    return "\n".join([x.name.replace(".txt", "") for x in get_user_prompt_directory().iterdir()])


def extract_number(filename):
    """Extracts a number from a filename using regular expressions.

    Args:
        filename: The name of the file.

    Returns:
        The extracted number, or None if no number is found.
    """
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else None


def get_files_between(folder_start, folder_transcript):
    """Gets a list of filenames between two folders based on the file numbering.

    Args:
        folder_start: The starting folder.
        folder_transcript: The ending folder.

    Returns:
        A list of filenames for each number between the two.
    """
    # List all files in the directories
    files_start = list(Path(folder_start).glob("*.wav.txt"))
    files_transcript = list(Path(folder_transcript).glob("*.wav.txt"))

    # Extract the file numbers and find the maximum
    numbers_start = [extract_number(f.stem) for f in files_start]
    numbers_transcript = [extract_number(f.stem) for f in files_transcript]

    max_start = max(numbers_start) if numbers_start else 1
    max_transcript = max(numbers_transcript) if numbers_transcript else 1

    # Generate filenames for each number between max_start and max_transcript
    filenames = [f"short{str(i).zfill(4)}.wav.txt" for i in range(max_start, max_transcript + 1)]

    return filenames
