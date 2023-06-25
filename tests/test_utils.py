# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""Tests for utils.py."""
import pytest  # noqa: F401

from afkode.utils import split_transcription_on


def test_split_transcription_on_after_strategy() -> None:
    """Test that the function correctly splits after the target word."""
    transcription = "This is a sample transcription. Target word is here. And there is some more text."
    word = "target"
    strategy = "after"
    expected_output = "word is here. And there is some more text."
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_before_strategy() -> None:
    """Test that the function correctly splits before the target word."""
    transcription = "This is a sample transcription. Target word is here. And there is some more text."
    word = "target"
    strategy = "before"
    expected_output = "This is a sample transcription"
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_after_twice_strategy() -> None:
    """Test that the function correctly splits after the second target word."""
    transcription = "Blep. First target word is here and second target is here. boop."
    word = "target"
    strategy = "after"
    expected_output = "is here. boop."
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_before_twice_strategy() -> None:
    """Test that the function correctly splits after the second target word."""
    transcription = "Blep. First target word is here and second target is here. boop."
    word = "target"
    strategy = "before"
    expected_output = "Blep. First"
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_invalid_strategy() -> None:
    """Test that the function raises an error for an invalid strategy."""
    transcription = "This is a sample transcription. Target word is here. And there is some more text."
    word = "target"
    strategy = "invalid"
    with pytest.raises(ValueError):
        split_transcription_on(transcription, word, strategy)


def test_split_transcription_on_case_insensitive_matching() -> None:
    """Test that the function correctly handles case-insensitive matching."""
    transcription = "This is a sample transcription. TARGET word is here. And there is some more text."
    word = "TARGET"
    strategy = "after"
    expected_output = "word is here. And there is some more text."
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_word_ignored_no_space() -> None:
    """Test that the function handles situations where the target word is immediately followed by another word without a space."""
    transcription = "This is a sample transcription.target word is here. And there is some more text."
    word = "target"
    strategy = "after"
    expected_output = "word is here. And there is some more text."
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_word_ignored_surrounded_text() -> None:
    """Test that the function handles situations where the target word is part of another word."""
    transcription = "This is a sample transcription. targeted word will be ignored."
    word = "target"
    strategy = "after"
    expected_output = "This is a sample transcription. targeted word will be ignored."
    assert split_transcription_on(transcription, word, strategy) == expected_output


def test_split_transcription_on_word_ignored_hyphenated() -> None:
    """Test that the function handles situations where the target word is hyphenated with the next word."""
    transcription = "This is a sample transcription. target-word is here. And there is some more text."
    word = "target"
    strategy = "after"
    expected_output = "word is here. And there is some more text."
    assert split_transcription_on(transcription, word, strategy) == expected_output
