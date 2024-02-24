# CTS Comand Line Interface App
This Python command-line interface application provides a convenient way to interact with the API of the Strasbourg's CTS transport company. It allows users to access various information related to public transportation services in Strasbourg, including real-time data on routes, schedules, stops, and more.

## Features
- Get departure time
## Requirements ✅
- Python 3.10.12
- You are required to have the token and password provided by CTS opendata. see https://www.cts-strasbourg.eu/fr/portail-open-data/
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
This command allows you to get the estimated departure time from a specific station.
You will interctively specify the station.
```sh
cts-cli departure-time
Usage: cts-cli departure-time [OPTIONS]

  Get the estimated departure time for a specific line, station, and
  destination.

Options:
  --help  Show this message and exit.
```
#### Example Usage
```sh
cts-cli departure-time
Enter station name: emile mathis
Departure at station: emile mathis Sat. 24 Feb 19:37
+------+----------------------+----------------+--------------+
| Line |     Destination      | Departure Time | Departure in |
+------+----------------------+----------------+--------------+
|  A   |    Graffenstaden     |    19:38:38    |   Arriving   |
|  A   |   Parc des Sports    |    19:39:43    |    2 min     |
|  E   | Robertsau - L'Escale |    19:40:36    |    3 min     |
|  E   |  Campus d'Illkirch   |    19:44:32    |    7 min     |
+------+----------------------+----------------+--------------+
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
