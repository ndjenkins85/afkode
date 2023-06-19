# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
'''meta-programming scripts to receive help from chatgpt on program improvements.'''

import logging
from pathlib import Path

# Any script entry must have this
# For it to work on pythonista
try:
    import set_env
except ModuleNotFoundError:
    from afkode import set_env

from afkode import utils


def get_readme() -> str:
    """Loads first portion of the project readme."""
    readme = Path(utils.get_base_path(), "README.md").read_text(encoding="utf-8")
    clean_readme = readme.split("## Contents")[0]
    return clean_readme


def start():
    logging.info(get_readme())


if __name__ == "__main__":
    utils.setup_logging(log_level=logging.INFO)
    start()
