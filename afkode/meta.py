# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""meta-programming scripts to receive help from chatgpt on program improvements."""

import argparse
import logging
from pathlib import Path

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env
except ModuleNotFoundError:
    from afkode import set_env

from afkode import api, utils


def get_readme() -> str:
    """Loads first portion of the project readme."""
    readme = Path(utils.get_base_path(), "README.md").read_text(encoding="utf-8")
    clean_readme = readme.split("## Contents")[0]
    return clean_readme


def clean_py(python_text: str) -> str:
    remove = "# -*- coding: utf-8 -*-\n" + Path(utils.get_base_path(), "LICENSE").read_text()
    clean_python_text = python_text.replace(remove, "")
    return clean_python_text


def start():
    logging.info(get_readme())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conduct analysis on your codebase")
    parser.add_argument("--prompt", type=str, help="The prompt string, or path to a prompt")
    parser.add_argument("--input_files", nargs="+", help="A list of input files")
    parser.add_argument("--execute", action="store_true", help="Execution flag")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    utils.setup_logging(log_level=log_level)

    input_files = utils.resolve_input_paths(args.input_files, exclude=["__init__.py"])
    args.prompt
    args.execute

    start()
