#! /usr/bin/env bash
set -euo pipefail

if [[ -d .git ]]; then
    git pull

fi

$1 -m pip install --upgrade pip
$1 -m pip install poetry
$1 -m poetry install
$1 -m poetry run python -m mcoding_bot
