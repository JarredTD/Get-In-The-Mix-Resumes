#!/bin/bash

SPHINX_PATH="build/tools/sphinx"

mkdir -p "$SPHINX_PATH"

source ./venv/bin/activate

make html 2>&1 | tee "$SPHINX_PATH/sphinx_output.txt"
open build/sphinx/html/index.html
