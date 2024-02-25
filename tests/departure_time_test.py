# -*- coding: utf-8 -*-
# pylint: skip-file
"""Departure time test module."""
from datetime import datetime, timedelta
import pytest
from cts_cli.api.departure_time import get_station_ref, get_station_departures


future_datetime = datetime.now() + timedelta(minutes=5)
formatted_datetime_str = future_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")

# Test cases for the happy path
happy_path_cases = [
    (
        "single_station_single_journey",
        {
            "ServiceDelivery": {
                "EstimatedTimetableDelivery": [
                    {
                        "EstimatedJourneyVersionFrame": [
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "12345",
                                                "StopPointName": "StationA",
                                            },
                                            {
                                                "StopPointRef": "67890",
                                                "StopPointName": "StationB",
                                            },
                                        ]
                                    }
                                ]
                            },
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "12345",
                                                "StopPointName": "StationA",
                                            },
                                            {
                                                "StopPointRef": "67890",
                                                "StopPointName": "StationB",
                                            },
                                        ]
                                    }
                                ]
                            },
                        ]
                    }
                ]
            }
        },
        "StationA",
        ["12345"],
    ),
    (
        "multiple_stations_multiple_journeys",
        {
            "ServiceDelivery": {
                "EstimatedTimetableDelivery": [
                    {
                        "EstimatedJourneyVersionFrame": [
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "12345",
                                                "StopPointName": "StationA",
                                            },
                                            {
                                                "StopPointRef": "67890",
                                                "StopPointName": "StationA",
                                            },
                                        ]
                                    },
                                ]
                            },
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "12345",
                                                "StopPointName": "StationA",
                                            },
                                            {
                                                "StopPointRef": "67890",
                                                "StopPointName": "StationA",
                                            },
                                        ]
                                    },
                                ]
                            },
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "54321",
                                                "StopPointName": "StationA",
                                            },
                                            {
                                                "StopPointRef": "09876",
                                                "StopPointName": "StationC",
                                            },
                                        ]
                                    }
                                ]
                            },
                        ]
                    }
                ]
            }
        },
        "StationA",
        ["12345", "67890", "54321"],
    ),
]

# Test cases for edge cases
edge_cases = [
    ("empty_json", {}, "StationA", KeyError),
    (
        "no_estimated_journey_version_frame",
        {"ServiceDelivery": {"EstimatedTimetableDelivery": [{}]}},
        "StationA",
        KeyError,
    ),
    (
        "no_estimated_vehicle_journey",
        {
            "ServiceDelivery": {
                "EstimatedTimetableDelivery": [{"EstimatedJourneyVersionFrame": [{}]}]
            }
        },
        "StationA",
        [],
    ),
    (
        "station_not_present",
        {
            "ServiceDelivery": {
                "EstimatedTimetableDelivery": [
                    {
                        "EstimatedJourneyVersionFrame": [
                            {
                                "EstimatedVehicleJourney": [
                                    {
                                        "EstimatedCalls": [
                                            {
                                                "StopPointRef": "12345",
                                                "StopPointName": "StationB",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        },
        "StationA",
        [],
    ),
]

# Test cases for error cases
error_cases = [
    ("invalid_json_structure", {"InvalidKey": {}}, "StationA", KeyError),
]


@pytest.mark.parametrize(
    "test_id, json_response, station_name, expected", happy_path_cases
)
def test_get_station_ref_happy_path(test_id, json_response, station_name, expected):
    """Test get_station_ref_happy."""
    # Act
    result = get_station_ref(json_response, station_name)

    # Assert
    assert result == expected, f"Failed {test_id}"


# @pytest.mark.parametrize("test_id, json_response, station_name, expected_exception", edge_cases)
# def test_get_station_ref_edge_cases(test_id, json_response, station_name, expected_exception):
#     # Act & Assert
#     with pytest.raises(expected_exception):
#         get_station_ref(json_response, station_name)


@pytest.mark.parametrize(
    "test_id, json_response, station_name, expected_exception", error_cases
)
def test_get_station_ref_error_cases(
    test_id, json_response, station_name, expected_exception
):
    """Test get station ref error cases."""
    # Act & Assert
    with pytest.raises(expected_exception):
        get_station_ref(json_response, station_name)


# Helper functions that would be used by the get_station_departures function
# These need to be defined for the tests to run successfully
def get_time_only(datetime_str):
    """Mock implementation of get_time_only."""
    return datetime_str.split("T")[1]


def get_remaining_minutes(datetime_str):
    """Mock implementation of get_remaining_minutes."""
    from datetime import datetime

    expected_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    now = datetime.now()
    return int((expected_time - now).total_seconds() // 60)


def format_minutes(minutes):
    """Mock implementation of format_minutes."""
    return f"{minutes} min"


# Parametrized test cases for the get_station_departures function
@pytest.mark.parametrize(
    "test_id, json_responses, expected_output",
    [
        # Happy path tests with various realistic test values
        (
            "happy-1",
            [
                {
                    "ServiceDelivery": {
                        "StopMonitoringDelivery": [
                            {
                                "MonitoredStopVisit": [
                                    {
                                        "MonitoredVehicleJourney": {
                                            "LineRef": "LineA",
                                            "DestinationName": "DestinationA",
                                            "MonitoredCall": {
                                                "ExpectedDepartureTime": formatted_datetime_str
                                            },
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            [
                [
                    "LineA",
                    "DestinationA",
                    (datetime.now() + timedelta(minutes=5)).strftime("%H:%M:%S"),
                    "5 min",
                ]
            ],
        ),
        # Edge cases
        ("edge-empty-list", [], []),
        (
            "edge-no-monitored-stop-visit",
            [{"ServiceDelivery": {"StopMonitoringDelivery": [{}]}}],
            [],
        ),
        # Error cases
        (
            "error-invalid-json-structure",
            [{}],  # Invalid JSON structure
            pytest.raises(KeyError),
        ),
        ("error-none-json-response", None, pytest.raises(TypeError)),
    ],
)
def test_get_station_departures(test_id, json_responses, expected_output):
    """Test get_station_departures."""
    # Arrange
    # (No arrange step needed as all input values are provided via test parameters)

    # Act
    if isinstance(expected_output, list):
        result = get_station_departures(json_responses)
    else:
        with expected_output:
            get_station_departures(json_responses)

    # Assert
    if isinstance(expected_output, list):
        assert result == expected_output
