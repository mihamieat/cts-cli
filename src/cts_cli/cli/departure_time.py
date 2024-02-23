# -*- coding: utf-8 -*-
"""Main module for the CTS cli app."""
import click
from src.cts_cli.api.departure_time import departure_time_call


@click.command()
@click.pass_context
def departure_time(ctx):
    """
    Get the estimated departure time for a specific line, station, and destination.
    """
    line = click.prompt("Enter line")
    destination = click.prompt("Enter line direction")
    station = click.prompt("Enter station name")
    try:
        dep_time = departure_time_call(
            ctx, line=line, station=station, destination=destination
        )
        click.echo(
            f"Estimated departure time for line {line} at {station} to {destination}: {dep_time}"
        )
    except IndexError as e:
        click.echo(f"Could not find data: {e}")
