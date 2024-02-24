# -*- coding: utf-8 -*-
"""Module for date and time related methods."""
from datetime import datetime


def today_date() -> str:
    """
    Get the current date and time in the format "Sat. 24 Feb. 19:30".

    Returns:
        str: The formatted current date and time.

    Examples:
        >>> today_date()
    """
    today = datetime.now()
    return today.strftime("%a. %d %b. %H:%M")
