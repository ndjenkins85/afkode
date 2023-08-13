# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Contains utility functions used throughout the AFKode project."""

import json
import logging
import os
import re
from datetime import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Union

try:
    import yaml
except ImportError:
    pass

from afkode import globals


def setup_logging(log_level: int = globals.LOG_LEVEL) -> None:
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
            handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f"Directory {log_path} missing, cannot create log file."
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)
    logging.info(globals.system_message)


def get_base_path() -> Path:
    """Helps to determine where to run file activities depending on env.

    Returns:
        Resolved base path of program
    """
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
    """Helper to find prompt directory.

    Returns:
        Resolved base path of prompt directory.
    """
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


def get_agent_response_directory() -> Path:
    """Retrieves the directory path for user input.

    Returns:
        The path to the user input directory.
    """
    agent_response_directory_path = Path(get_base_path(), "data", "agent_response")
    if not agent_response_directory_path.exists():
        agent_response_directory_path.mkdir(parents=True)
    return agent_response_directory_path


def get_user_prompt_files() -> str:
    """Retrieves a string of all the filenames in the user input directory.

    Returns:
        The string of filenames.
    """
    return "\n".join([x.name.replace(".txt", "") for x in get_user_prompt_directory().iterdir()])


def extract_number(filename: str) -> int:
    """Extracts a number from a filename using regular expressions.

    Args:
        filename: The name of the file.

    Returns:
        The extracted number, or None if no number is found.
    """
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


def resolve_input_paths(input_files: List[str], exclude: List[str] = None) -> List[Path]:
    """Given a list of file paths, test and resolve them.

    Args:
        input_files: The list of input file paths.
        exclude: The list of files to exclude. Default is None.

    Returns:
        The list of resolved paths.
    """
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
            partly_resolved = sorted(list(Path(get_base_path(), "afkode", folder).glob(glob)))
        else:
            partly_resolved = [Path(get_base_path(), "afkode", inp)]

        for pr in partly_resolved:
            if pr and pr.name not in exclude:
                resolved.append(pr)
    return resolved


def get_formatted_command_list() -> str:
    """Parses the command folder and produces a simple list of commands.

    Returns:
        Cleaned up string with 'filename - description'
    """
    # Get all commands ready for a prompt
    command_dir = Path(get_base_path(), "afkode", "commands")
    ignore = ["__init__"]
    command_files = [f.stem for f in command_dir.glob("*.py") if f.stem not in ignore]

    options = ""
    for command_file in command_files:
        options += f"Filename: {command_file} - Description: "
        command_data = Path(command_dir, f"{command_file}.py").read_text(encoding="utf-8")
        # Use the start of the docstring as the description
        description_start_tag = ' -> str:\n    """'
        description_end_tag = "    Args:"
        try:
            description = (
                command_data.split(description_start_tag)[1]
                .split(description_end_tag)[0]
                .replace("\n", "")
                .replace("  ", " ")
            )
        except Exception:
            logging.warning(f"Could not parse {command_file} in standard way")
            return ""
        options += description + "\n"
    return options


def split_transcription_on(transcription: str, words: Union[str, List[str]], strategy: str = "after") -> str:
    """Uses regex matching based on case-insensitive, matched word boundaries to split text before or after.

    * It matches the exact word you're looking for, bounded by non-word characters or the beginning/end of the string.
    * It splits the transcription at these word boundaries.
    * If strategy is "after", it takes everything after the last occurrence of the word.
    * If strategy is "before", it takes everything before the first occurrence of the word.
    * If strategy is "detect", it will remove the word; this can be tested as a length difference
    * If the word is part of a larger word it doesn't match.
    * Case insensitive

    Args:
        transcription: raw transcription text
        words: single or list of keywords to search and split on
        strategy: whether to return text before or after the word

    Raises:
        ValueError: if an invalid strategy selected

    Returns:
        Cleaned transcription text that focuses on info between keywords
    """
    # If no word, bypass this whole thing
    if words == "":
        return transcription
    if isinstance(words, str):
        words = [words]
    pattern = r"[\W]*\b{}\b[\W]*".format("|".join(map(re.escape, words)))
    split_text = re.split(pattern, transcription, flags=re.IGNORECASE)
    if strategy == "after":
        clean_transcription = split_text[-1].strip()
    elif strategy == "before":
        clean_transcription = split_text[0].strip()
    elif strategy == "detect":
        clean_transcription = " ".join(split_text).strip()
    else:
        raise ValueError("Invalid strategy")
    return clean_transcription


def load_config() -> Dict[str, Any]:
    """Load the config file for basic behaviour change.

    Returns:
        Basic dictionary with user facing options.
    """
    config_path = Path(get_base_path(), "afkode", "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


def get_spoken_command_list() -> List[str]:
    """Get cleaned up simple list of actions.

    Returns:
        List of cleaned up actions
    """
    command_dir = Path(get_base_path(), "afkode", "commands")
    ignore = ["__init__"]
    command_files = sorted([f.stem.replace("_", " ") for f in command_dir.glob("*.py") if f.stem not in ignore])
    return command_files


def load_config(input_path_raw: Union[Path, str]) -> Dict[str, Any]:
    """Loads and checks an input config file.

    Args:
        input_path: Location of yaml file relative to working directory.

    Returns:
        Program configuration instructions in JSON compatable format
    """
    input_path: Path = Path(input_path_raw)
    fully_resolved_path = Path(get_base_path(), input_path)
    if not fully_resolved_path.exists():
        message = f"Cannot locate input file at {fully_resolved_path}"
        logging.error(message)
        raise ValueError(message)

    if ".yaml" in input_path.suffix or ".yml" in input_path.suffix:
        logging.info(f"Loading YAML config from {input_path}")
        with input_path.open() as fp:
            config = yaml.safe_load(fp)
    else:
        message = f"Incompatable file type {input_path.suffix}, expected SQL, JSON, or YAML"
        logging.error(message)
        raise ValueError(message)

    _check_config_format(config)
    logging.debug(f"Config: {config}")
    return config


def _check_config_format(config: Dict[str, Any]) -> bool:
    """Ensure config conforms to format requirements."""
    return True


def resolve_paths(paths_list: List[str]) -> List[Path]:
    """Assesses which input folders and files are specified in config.

    Args:
        config: Standard config used in project

    Returns:
        A flat list of all file paths specified in config
    """    
    resolved_paths = []
    for path in paths_list:
        if Path(path).parts[0] == '/':
            file_path = str(Path(*Path(path).parts[1:]))
        else:
            file_path = path

        file_paths = list(Path('/').glob(str(file_path)))

        if len(file_paths) == 0:
            message = f"Could not find any files at {path}"
            logging.error(message)
            raise ValueError(message)

        for file_path in file_paths:
            if not file_path.exists():
                message = "Could not find file at specified location"
                logging.error(message)
                raise ValueError(message)        
            resolved_paths.append(file_path)
    return resolved_paths
