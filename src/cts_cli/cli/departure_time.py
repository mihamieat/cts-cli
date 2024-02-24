# -*- coding: utf-8 -*-
"""Module for the departure time command."""
import click
from cts_cli.api.departure_time import departure_time_call
from cts_cli.display.departure_time import display_departure_time


@click.command()
@click.pass_context
def departure_time(ctx):
    """
    Get the estimated departure times for every lines that stops at a given station.
    """
    station = click.prompt("Enter station name")
    try:
        dep_time = departure_time_call(ctx, station=station)
        table = display_departure_time(departure_time=dep_time)
        click.echo(f"Departure at station: \033[1m{station}\033[0m\n{table}")
    except IndexError as e:
        click.echo(f"Could not find data for {station}, check spelling: {e}")
