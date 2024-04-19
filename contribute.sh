#!/bin/bash

python -m ensurepip
curl -sSL https://bootstrap.pypa.io/get-pip.py | python -
python -m pip install --user poetry
poetry lock
poetry install
python -m pip install --user pre-commit
pre-commit install
