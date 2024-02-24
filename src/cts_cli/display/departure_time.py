# -*- coding: utf-8 -*-
"""Departure time display module."""
from prettytable import PrettyTable


table = PrettyTable()


def display_departure_time(departure_time: list[dict]) -> str:
    """
    Display the departure time information in a formatted table.

    Args:
        departure_time (list[dict]): A list of dictionaries representing \
the departure time information.

    Returns:
        str: The formatted table as a string.
    """
    labels = ["Line", "Destination", "Departure Time", "Departure in"]
    table.field_names = labels
    table.add_rows(departure_time)

    return table
