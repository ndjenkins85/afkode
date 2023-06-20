# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains utility functions used throughout the AFKode project."""

import logging
import os
import re
import time
from datetime import datetime as dt
from pathlib import Path
from typing import List

from afkode.globals import *


def setup_logging(log_level=logging.DEBUG) -> None:
    """Configures the logging settings for the application.

    Args:
        log_level: The log level to set. Default is DEBUG.
    """
    log_base = Path(get_base_path(), "logs")
    if not log_base.exists():
        log_base.mkdir()
    log_path = Path(log_base, f"{str(dt.now())}.txt")
    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f"Directory {log_path} missing, cannot create log file."
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)


def get_base_path():
    """Helps to determine where to run file activities depending on env"""
    try:
        import importlib_resources

        folder_parts = importlib_resources.files("afkode").parts

        # Installed version
        if "site-packages" in folder_parts:
            base_path = Path(Path.home(), ".afkode")
            if not base_path.exists():
                logging.info(f"Creating user data directory at {base_path}")
                base_path.mkdir()
        # Import / dev version
        else:
            base_path = Path(*importlib_resources.files("afkode").parts[:-1])
    except ModuleNotFoundError:
        # Pythonista version
        base_path = Path(*Path(os.getcwd()).parts[:-1])
    return base_path


def get_prompt_path() -> Path:
    """Helper to find prompt directory"""
    try:
        import importlib_resources

        base_path = Path(*importlib_resources.files("afkode").parts[:-1], "afkode", "prompts")
    except ModuleNotFoundError:
        # Pythonista version
        base_path = Path(*Path(os.getcwd()).parts[:-1], "afkode", "prompts")
    return base_path


def get_user_prompt_directory() -> Path:
    """Retrieves the directory path for user input.

    Returns:
        The path to the user input directory.
    """
    user_prompt_directory_path = Path(get_base_path(), "data", "user_response")
    if not user_prompt_directory_path.exists():
        user_prompt_directory_path.mkdir(parents=True)
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


def resolve_input_paths(input_files: List[str], exclude: List[str] = None) -> List[Path]:
    """Given a list of file paths, test and resolve them."""
    if not exclude:
        exclude = []
    if not input_files:
        return []
    resolved = []
    for inp in input_files:
        if "*" in inp:
            if "/**/" in inp:
                folder, search = inp.split("/**/")
                glob = "**/" + search
            elif "/*" in inp:
                folder, search = inp.split("/*")
                glob = "*" + search
            partly_resolved = sorted(list(Path(utils.get_base_path(), "afkode", folder).glob(glob)))
        else:
            partly_resolved = list(Path(utils.get_base_path(), "afkode", inp))

        for pr in partly_resolved:
            if pr and pr.name not in exclude:
                resolved.append(pr)
    return resolved
