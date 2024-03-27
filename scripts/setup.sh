#!/bin/bash

python3 -m venv venv
source ./venv/bin/activate
pip3 install -r src/dev-requirements.txt
pre-commit install
