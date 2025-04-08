# -*- coding: utf-8 -*-
"""Module for gathering all commands."""
import sys
import click
from decouple import Config, config, UndefinedValueError

from cts_cli.cli.departure_time import departure_time

file_config = Config(".env.dev")
API_URL = config("API_URL", default="https://api.cts-strasbourg.eu")
API_VERSION = config("API_VERSION", default="v1")
try:
    TOKEN = config("TOKEN")
except UndefinedValueError as e:
    click.echo(f"⚠️ Missing TOKEN in environment variables: {e}")
try:
    PASSWORD = config("PASSWORD")
except UndefinedValueError as e:
    click.echo(f"⚠️ Missing PASSWORD in environment variables: {e}")


@click.group()
@click.pass_context
def cli(ctx):
    """Command line interface app for CTS API."""
    try:
        ctx.obj = {
            "url": f"{API_URL}/{API_VERSION}/siri/2.0",
            "token": TOKEN,
            "password": PASSWORD,
        }
    except NameError as nameerror:
        click.echo(f"Missing one required environment variable: {nameerror}")
        sys.exit(1)


cli.add_command(departure_time)
