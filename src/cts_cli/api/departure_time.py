# -*- coding: utf-8 -*-
"""Main module for the CTS cli app."""
from datetime import datetime

import click
import requests

ENDPOINT = "/estimated-timetable"
TIMEOUT = 10


def departure_time_call(ctx, line: str, station: str, destination: str):
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
    full_url = f"{ctx.obj.get('url')}{ENDPOINT}"
    print(full_url)
    response = requests.get(
        url=full_url,
        auth=(ctx.obj.get("token"), ctx.obj.get("password")),
        timeout=TIMEOUT,
    )
    try:
        estimated_journey_version_frame = response.json()["ServiceDelivery"][
            "EstimatedTimetableDelivery"
        ][0]["EstimatedJourneyVersionFrame"]
    except KeyError as e:
        click.echo(f"Error. No estimated journey version frame found: {str(e)}")
    for journey_frame in estimated_journey_version_frame:
        line_station = [
            journey
            for journey in journey_frame["EstimatedVehicleJourney"]
            if journey["LineRef"] == line
        ]
        if line_station:
            break
    datetime_str = [
        call
        for call in line_station[0]["EstimatedCalls"]
        if call["StopPointName"].lower() == station.lower()
        and call["DestinationName"].lower() == destination.lower()
    ][0]["ExpectedDepartureTime"]

    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
