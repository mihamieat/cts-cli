# CTS Comand Line Interface App
This Python command-line interface application provides a convenient way to interact with the API of the Strasbourg's CTS transport company. It allows users to access various information related to public transportation services in Strasbourg, including real-time data on routes, schedules, stops, and more.

## Features
- Get departure time
## Installation ⚙️
```sh
pip install git+https://github.com/mihamieat/cts-cli
```
## Set the environment variables 🔧
Following variables are mandatory. They could be set in a .env file.
| Variable  | Purpose  | Default value |
|---|---|---|
| API_URL  | URL of the API  | https://api.cts-strasbourg.eu |
|  API_VERSION | Version of the API  | v1 |
| TOKEN  |  Username token | |
| PASSWORD | Associated password  | |
## Run the CLI 🚀
```sh
cts-cli
Usage: cts-cli [OPTIONS] COMMAND [ARGS]...

  Command line interface app for CTS API.

Options:
  --help  Show this message and exit.

Commands:
  departure-time  Get the estimated departure time for a specific line,...
```
### Departure Time
This command allows you to get the estimated departure time from a specific station of a line that goes towards the line destination.
You will interctively specify the line, the line direction, and the station.
```sh
cts-cli departure-time
Usage: cts-cli departure-time [OPTIONS]

  Get the estimated departure time for a specific line, station, and
  destination.

Options:
  --help  Show this message and exit.
```
## Contribute 👩🏻‍🔬
### Clone the project
```sh
git clone https://github.com/mihamieat/cts-cli
```
### Intstall development tools
#### Poetry
See https://python-poetry.org/docs/
```sh
pipx install poetry==1.2.0
poetry install
```
To test changes, run:
```sh
poetry run cts-cli [OPTIONS] COMMAND [ARGS]...
```
#### Pre-commit
See https://pre-commit.com
```sh
pipx install pre-commit
```

## License 📄
This project is licensed under the terms of the MIT License.

## Author
Mihamina Rakotovazaha r.miham@yahoo.com
