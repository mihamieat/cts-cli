# -*- coding: utf-8 -*-
"""Module for gathering all commands."""
import click
from decouple import Config, config

from cts_cli.cli.departure_time import departure_time

file_config = Config(".env.dev")
API_URL = config("API_URL", default="https://api.cts-strasbourg.eu")
API_VERSION = config("API_VERSION", default="v1")
TOKEN = config("TOKEN")
PASSWORD = config("PASSWORD")


@click.group()
@click.pass_context
def cli(ctx):
    """Command line interface app for CTS API."""
    ctx.obj = {
        "url": f"{API_URL}/{API_VERSION}/siri/2.0",
        "token": TOKEN,
        "password": PASSWORD,
    }


cli.add_command(departure_time)
