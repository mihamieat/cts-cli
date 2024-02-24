# -*- coding: utf-8 -*-
"""Module for all departure time functions related."""
from datetime import datetime, timezone
import math
from icecream import ic

import click
import requests

ESTIMATED_TIMETABLE_ENDPOINT = "/estimated-timetable"
STOP_MONITORING_ENDPOINT = "/stop-monitoring"
TIMEOUT = 10


def departure_time_call(ctx, station: str) -> str:
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
    et_url = f"{ctx.obj.get('url')}{ESTIMATED_TIMETABLE_ENDPOINT}"
    et_response = requests.get(
        url=et_url,
        auth=(ctx.obj.get("token"), ctx.obj.get("password")),
        timeout=TIMEOUT,
    )
    station_refs = get_station_ref(et_response.json(), station)
    ic(station_refs)

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
    try:
        estimated_journey_version_frame = json_response["ServiceDelivery"][
            "EstimatedTimetableDelivery"
        ][0]["EstimatedJourneyVersionFrame"][1:]
    except KeyError as e:
        click.echo(f"Error. No estimated journey version frame found: {str(e)}")
    station_refs = []
    for estimated_journey in estimated_journey_version_frame:
        for journey in estimated_journey["EstimatedVehicleJourney"]:
            line_station = [
                station
                for station in journey["EstimatedCalls"]
                if station["StopPointName"].lower() == station_name.lower()
            ]
        if line_station:
            station_refs.append(line_station[0]["StopPointRef"])
    return list(filter(None, station_refs))


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
    return [
        [
            stop["MonitoredVehicleJourney"]["LineRef"],
            stop["MonitoredVehicleJourney"]["DestinationName"],
            stop["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedDepartureTime"],
            get_remaining_minutes(
                stop["MonitoredVehicleJourney"]["MonitoredCall"][
                    "ExpectedDepartureTime"
                ]
            ),
        ]
        for stop in merged_stop_visits
    ]


def get_remaining_minutes(given_datetime_str: str) -> str:
    """
    Get the remaining minutes between the given datetime and the current datetime.

    Args:
        given_datetime_str (str): The given datetime string in ISO format.

    Returns:
        str: The remaining minutes as a string.

    Examples:
        >>> get_remaining_minutes("2022-01-01T12:00:00")
        '123 min'
    """
    given_datetime = datetime.fromisoformat(given_datetime_str)
    current_datetime = datetime.now(timezone.utc)
    time_difference = (given_datetime - current_datetime).total_seconds() / 60
    return (
        f"{math.ceil(time_difference)} min"
        if time_difference > 1
        else "\033[32mArriving\033[0m"
    )
