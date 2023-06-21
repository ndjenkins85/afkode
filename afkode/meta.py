# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""meta-programming scripts to receive help from chatgpt on program improvements."""

import argparse
import logging
from pathlib import Path
from typing import List

# Any script entry must have this to work on iOS
# and we can use it for alternative importing
try:
    import set_env  # noqa: F401
except ModuleNotFoundError:
    from afkode import set_env  # noqa: F401

from afkode import api, utils


def get_formatted_readme() -> str:
    """Loads first portion of the project readme.

    Returns:
        Cleaned up readme string only taking first part.
    """
    readme = Path(utils.get_base_path(), "README.md").read_text(encoding="utf-8")
    clean_readme = readme.split("## Contents")[0]
    return clean_readme


def clean_py(python_text: str) -> str:
    """Loads first portion of the project readme.

    Args:
        python_text: input text of loaded python file

    Returns:
        Removes top text from file
    """
    remove = "# -*- coding: utf-8 -*-\n# Copyright © 2023 by Nick Jenkins. All rights reserved"
    clean_python_text = python_text.replace(remove, "")
    return clean_python_text


def start(prompt: str = None, input_files: List[Path] = None, execute: bool = False) -> None:
    """Conduct an adhoc analysis on the codebase.

    Args:
        prompt: text of the LLM prompt
        input_files: list of paths to include in the prompt
        execute: whether to run on LLM or not
    """
    request = ""
    if prompt:
        request += prompt + "\n"
    if not input_files:
        input_files = []
    for input_file in input_files:
        if input_file.stem == "README":
            clean = get_formatted_readme()
        else:
            clean = clean_py(input_file.read_text(encoding="utf-8"))
        request += f"File: {str(input_file)} ****\n"
        request += clean + "\n\n"

    logging.info(f"Request: {request}")
    if execute:
        response = api.chatgpt(request, "gpt-3.5-turbo-16k")
        logging.info(f"Response: {response}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conduct analysis on your codebase")
    parser.add_argument("--prompt_text", type=str, help="Prompt string")
    parser.add_argument("--prompt_path", type=str, help="Path to a prompt")
    parser.add_argument("--input_files", nargs="+", help="A list of input files")
    parser.add_argument("--execute", action="store_true", help="Execution flag")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    utils.setup_logging(log_level=log_level)

    input_files = utils.resolve_input_paths(args.input_files, exclude=["__init__.py"])

    if args.prompt_text:
        prompt = args.prompt_text
    elif args.prompt_path:
        prompt_path = Path(utils.get_base_path(), args.prompt_path)
        if prompt_path.exists():
            prompt = Path(utils.get_base_path(), args.prompt_path).read_text(encoding="utf-8")
        else:
            logging.warning(f"Cannot find prompt_path: {prompt_path}")
    else:
        prompt = None

    start(prompt=prompt, input_files=input_files, execute=args.execute)
