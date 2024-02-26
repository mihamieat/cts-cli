# -*- coding: utf-8 -*-
"""Suggestion mechanism module."""
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from icecream import ic


def suggester(prompt_txt: str):
    """Provide input suggestions or autocomplete functionality."""
    suggestions = ["Emile Mathis", "Parc des Sports"]
    completer = WordCompleter(suggestions)
    return prompt(prompt_txt, completer=completer)


def collect_values_from_key(dictionary, key):
    """Recursively collect values from a key in a dictionary."""
    values = []

    def _collect_values(dictionary) -> list:
        if isinstance(dictionary, dict):
            if key in dictionary:
                values.append(dictionary[key])
            for value in dictionary.values():
                _collect_values(value)
        elif isinstance(dictionary, list):
            for item in dictionary:
                _collect_values(item)

    _collect_values(dictionary)
    ic(values)
    return list(set(values))
