# -*- coding: utf-8 -*-
"""Module for the departure time command."""
import click
from cts_cli.api.departure_time import departure_time_call, get_estimated_time_raw_data
from cts_cli.display.departure_time import display_departure_time
from cts_cli.display.datesandtimes import today_date
from cts_cli.utils.suggester import suggester


@click.command()
@click.pass_context
def departure_time(ctx):
    """
    Get the estimated departure times for every lines that stops at a given station.
    """
    estimated_time_data = get_estimated_time_raw_data(ctx)
    station = suggester("Enter station name: ", estimated_time_data)
    try:
        dep_time = departure_time_call(
            ctx, station=station, estimated_time_data=estimated_time_data.json()
        )
        table = display_departure_time(departure_time=dep_time)
        click.echo(
            f"Departure at station: \033[34m{station}\033[0m {today_date()}\n{table}"
        )
    except IndexError as e:
        click.echo(f"Could not find data for {station}, check spelling: {e}")
