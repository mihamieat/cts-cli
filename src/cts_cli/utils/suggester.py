# -*- coding: utf-8 -*-
"""Suggestion mechanism module."""
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def suggester(prompt_txt: str, response_json: dict):
    """Provide input suggestions or autocomplete functionality."""
    suggestions = collect_sation_names(response_json)
    completer = WordCompleter(suggestions, ignore_case=True)
    return prompt(prompt_txt, completer=completer)


def collect_sation_names(respons_json: dict) -> list:
    """Recursively collect Stop point names for responses."""
    stop_point_names = []
    for timetable in respons_json.json()["ServiceDelivery"][
        "EstimatedTimetableDelivery"
    ]:
        for frame in timetable["EstimatedJourneyVersionFrame"]:
            for journey in frame["EstimatedVehicleJourney"]:
                stop_point_names.extend(
                    call["StopPointName"] for call in journey["EstimatedCalls"]
                )
    return list(set(stop_point_names))
