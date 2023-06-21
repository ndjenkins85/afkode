# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved
"""Custom command."""

from pathlib import Path

from afkode import utils


def execute(keyword: str) -> str:
    """The user wants to search through their transcriptions with a keyword or phrase.

    Args:
        keyword: optional_additional_instructions

    Returns:
        response searching files
    """
    text_files = [x for x in Path(utils.get_base_path(), "data", "user_response").glob("*.txt")]

    results = {}
    for file in text_files:
        content = file.read_text(encoding="utf-8")
        if keyword.lower() in content.lower():
            results[file.name] = content

    if results:
        return f"Keyword {keyword} found in following files: {', '.join(results.keys())}"
    else:
        return f"No results found for keyword: {keyword}"
