#!/bin/bash
set -euo pipefail

if [[ -d .git ]]; then
    git pull

fi

$1 -m pip install --upgrade pip
$1 -m pip install poetry
$1 -m poetry install

while true
do
    $1 -m poetry run python -m mcoding_bot

    echo "CTRL+C to shutdown..."
    sleep 5
done
