# -*- coding: utf-8 -*-
# pylint: skip-file
"""Departure time function test module."""
import pytest
from unittest.mock import Mock, patch
from cts_cli.api.departure_time import departure_time_call

# Constants used for testing
STOP_MONITORING_ENDPOINT = "/stopMonitoring"
TIMEOUT = 10


# Test cases
@pytest.mark.parametrize(
    "test_id, ctx, station, estimated_time_data, expected_result",
    [
        # Happy path tests with various realistic test values
        (
            "happy-1",
            Mock(
                obj={
                    "url": "http://api.example.com",
                    "token": "token123",
                    "password": "pass123",
                }
            ),
            "Central",
            {"data": "dummy_data"},
            "expected_departures_1",
        ),
        # Add more happy path test cases here
        # Edge cases
        # Add edge cases here
        # Error cases
        # Add error cases here
    ],
)
def test_departure_time_call(
    test_id, ctx, station, estimated_time_data, expected_result
):
    # Arrange
    with patch(
        "cts_cli.api.departure_time.get_station_ref"
    ) as mock_get_station_ref, patch(
        "cts_cli.api.departure_time.requests.get"
    ) as mock_requests_get, patch(
        "cts_cli.api.departure_time.get_station_departures"
    ) as mock_get_station_departures:
        # Setup mock return values
        mock_get_station_ref.return_value = ["station_ref_1"]
        mock_requests_get.return_value = Mock(json=lambda: {"data": "response_data"})
        mock_get_station_departures.return_value = expected_result

        # Act
        result = departure_time_call(ctx, station, estimated_time_data)

        # Assert
        assert result == expected_result
        mock_get_station_ref.assert_called_once_with(estimated_time_data, station)
        mock_requests_get.assert_called_once()
        mock_get_station_departures.assert_called_once_with([{"data": "response_data"}])
