# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

import logging
import time
from pathlib import Path

from ai_cookie.globals import *


def setup_logging(log_level=logging.DEBUG) -> None:
    """Setup basic logging to path."""
    log_path = Path("logs", "_log.txt")
    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f"""Directory '{log_path}' missing, cannot create log file.
                  Make sure you are running from base of repo, with correct data folder structure.
                  Continuing without log file writing."""
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)


def running_on_pythonista() -> bool:
    try:
        import console

        logging.info("Running on iOS (pythonista)")
        return True
    except ModuleNotFoundError:
        logging.info("Running on MacOS (poetry-python)")
        return False


def get_user_prompt_directory() -> Path:
    """Simple retrieve of directory."""
    user_prompt_directory_path = Path("data", "user_response")
    if not user_prompt_directory_path.exists():
        user_prompt_directory_path.mkdir()
    return user_prompt_directory_path


def get_user_prompt_files() -> str:
    return "\n".join([x.name.replace(".txt", "") for x in get_user_prompt_directory().iterdir()])
