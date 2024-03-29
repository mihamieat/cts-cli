# -*- coding: utf-8 -*-
"""Module for all departure time functions related."""
from datetime import datetime, timezone
import math

import requests

from cts_cli.utils.loader import Loader

ESTIMATED_TIMETABLE_ENDPOINT = "/estimated-timetable"
STOP_MONITORING_ENDPOINT = "/stop-monitoring"
TIMEOUT = 10


@Loader(desc="Collecting estimated timetable data.")
def get_estimated_time_raw_data(ctx) -> dict:
    """
    Retrieves the estimated time raw data from the API.

    Args:
        ctx: The context object.

    Returns:
        dict: The raw data of the estimated time.

    Raises:
        None.

    Examples:
        >>> ctx = Context()
        >>> get_estimated_time_raw_data(ctx)
        {'key': 'value'}
    """
    et_url = f"{ctx.obj.get('url')}{ESTIMATED_TIMETABLE_ENDPOINT}"
    return requests.get(
        url=et_url,
        auth=(ctx.obj.get("token"), ctx.obj.get("password")),
        timeout=TIMEOUT,
    )


@Loader(desc="Collecting departure times data. 🚋 🚌")
def departure_time_call(ctx, station: str, estimated_time_data: dict) -> str:
    """
    Get the departure time for a specific line, station, and destination.

    Args:
        url (str): The URL to make the API request.
        token (str): The authentication token for the API.
        user (str): The user identifier.
        line (str): The line reference.
        station (str): The name of the station.
        destination (str): The name of the destination.

    Returns:
        dict: The departure information for the specified line, station, and destination.
    """
    et_response = estimated_time_data
    station_refs = get_station_ref(et_response, station)

    sm_urls = [
        f"{ctx.obj.get('url')}{STOP_MONITORING_ENDPOINT}?MonitoringRef={station_ref}"
        for station_ref in station_refs
    ]

    responses_json = list(
        map(
            lambda url: requests.get(
                url=url,
                auth=(ctx.obj.get("token"), ctx.obj.get("password")),
                timeout=TIMEOUT,
            ).json(),
            sm_urls,
        )
    )
    return get_station_departures(responses_json)


def get_station_ref(json_response: dict, station_name: str) -> list:
    """
    Get the reference IDs of a station from the JSON response.

    Args:
        json_response (dict): The JSON response containing the station information.
        station_name (str): The name of the station.

    Returns:
        list: A list of reference IDs of the station.

    Raises:
        KeyError: If no estimated journey version frame is found in the JSON response.

    Examples:
        >>> json_response = {"ServiceDelivery": {"EstimatedTimetableDelivery": \
[{"EstimatedJourneyVersionFrame": ...}]}}
        >>> get_station_ref(json_response, "StationA")
        ['12345', '67890']
    """
    station_name_cf = station_name.casefold()
    return [
        call["StopPointRef"]
        for ejv in json_response["ServiceDelivery"]["EstimatedTimetableDelivery"][0][
            "EstimatedJourneyVersionFrame"
        ][1:]
        for ej in ejv["EstimatedVehicleJourney"]
        for call in ej["EstimatedCalls"]
        if call["StopPointName"].casefold() == station_name_cf
    ]


def get_station_departures(json_responses: list[dict]) -> list:
    """
    Get the list of station departures from multiple JSON responses.

    Args:
        json_responses (list[dict]): A list of JSON responses containing the station departures.

    Returns:
        list: A list of lists representing the station departures, each containing the line, \
destination,
        expected departure time, and remaining minutes.

    Examples:
        >>> json_responses = [
        ...     {"ServiceDelivery": {"StopMonitoringDelivery": [{"MonitoredStopVisit": ...}]}},
        ...     ...
        ... ]
        >>> get_station_departures(json_responses)
        [
            ["LineA", "DestinationA", "10:30 AM", "5 min"],
            ...
        ]
    """
    monitored_stop_visits = [
        monitored_stop_visit["ServiceDelivery"]["StopMonitoringDelivery"][0][
            "MonitoredStopVisit"
        ]
        for monitored_stop_visit in json_responses
        if monitored_stop_visit["ServiceDelivery"]["StopMonitoringDelivery"][0].get(
            "MonitoredStopVisit"
        )
    ]
    merged_stop_visits = [item for sublist in monitored_stop_visits for item in sublist]
    schedules = [
        [
            stop["MonitoredVehicleJourney"]["LineRef"],
            stop["MonitoredVehicleJourney"]["DestinationName"],
            get_time_only(
                stop["MonitoredVehicleJourney"]["MonitoredCall"][
                    "ExpectedDepartureTime"
                ]
            ),
            get_remaining_minutes(
                stop["MonitoredVehicleJourney"]["MonitoredCall"][
                    "ExpectedDepartureTime"
                ]
            ),
        ]
        for stop in merged_stop_visits
    ]

    # delete duplicates
    schedules = [list(x) for x in {tuple(sublist) for sublist in schedules}]

    # add min prefix to minutes integers and get the 15 first lines
    schedules = sorted(schedules, key=lambda x: x[3])[:15]
    for schedule in schedules:
        schedule[3] = format_minutes(schedule[3])

    return schedules


def get_time_only(date_str: str) -> str:
    """
    Get the time component from a date string.
    """
    datetime_obj = datetime.fromisoformat(date_str)
    return datetime_obj.time().strftime("%H:%M:%S")


def get_remaining_minutes(given_datetime_str: str) -> str:
    """
    Get the remaining minutes between the given datetime and the current datetime.

    Args:
        given_datetime_str (str): The given datetime string in ISO format.

    Returns:
        str: The remaining minutes as a string.

    Examples:
        >>> get_remaining_minutes("2022-01-01T12:00:00")
        '13 min'
    """
    # Convert the given datetime string to a timezone-aware datetime object
    given_datetime = datetime.fromisoformat(given_datetime_str).astimezone(timezone.utc)

    # Get the current datetime (timezone-aware)
    current_datetime = datetime.now(timezone.utc)

    # Calculate the time difference in minutes
    time_difference = (given_datetime - current_datetime).total_seconds() / 60
    return math.ceil(time_difference)


def format_minutes(minutes: int):
    """
    Format the number of minutes into a human-readable string.
    """
    return f"{math.ceil(minutes)} min" if minutes > 1 else "\033[32mArriving\033[0m"
