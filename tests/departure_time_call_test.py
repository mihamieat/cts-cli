# -*- coding: utf-8 -*-
# pylint: skip-file
"""Departure time function test module."""
import pytest
from unittest.mock import patch
from cts_cli.api.departure_time import departure_time_call

# Constants used in the function, which should be defined in the actual code
ESTIMATED_TIMETABLE_ENDPOINT = "/estimated-timetable"
STOP_MONITORING_ENDPOINT = "/stop-monitoring"
TIMEOUT = 10


class MockContext:
    """Mock context and function to simulate external dependencies"""

    def __init__(self, url, token, password):
        self.obj = {"url": url, "token": token, "password": password}


def get_station_ref(response_json, station):
    """Mock funtion for get_station_ref."""
    return "ABC123"


def get_station_departures(response_json):
    """Mock funtion for get station departure."""
    return [
        ["A", "Parc des Sports", "18:12:45", "\x1b[32mArriving\x1b[0m"],
        ["E", "Robertsau - L'Escale", "18:21:21", "10 min"],
        ["A", "Graffenstaden", "18:21:42", "10 min"],
    ]


# Parametrized test cases
@pytest.mark.parametrize(
    "ctx, station, expected_departure_info, test_id",
    [
        # Happy path tests
        (
            MockContext("http://api.example.com", "token123", "password123"),
            "Central",
            {"departures": [["A", "Graffenstaden", "18:21:42", "10 min"]]},
            "happy_path_central",
        ),
        # Add more happy path test cases with different realistic values
        # Edge cases
        # Add edge cases here
        # Error cases
        # Add error cases here
    ],
)
def test_departure_time_call(ctx, station, expected_departure_info, test_id):
    """Run tests."""
    # Arrange
    with patch("requests.get") as mock_get, patch(
        "cts_cli.api.departure_time.get_station_ref"
    ) as mock_get_station_ref, patch(
        "cts_cli.api.departure_time.get_station_departures"
    ) as mock_get_station_departures:
        # Setup mock responses and return values
        mock_get.return_value.json.return_value = {}
        mock_get_station_ref.return_value = ["station_ref"]
        mock_get_station_departures.return_value = expected_departure_info

        # Act
        actual_departure_info = departure_time_call(ctx, station)

        # Assert
        assert actual_departure_info == expected_departure_info
        mock_get.assert_called()
        mock_get_station_ref.assert_called_with({}, station)
        mock_get_station_departures.assert_called_with([{}])
