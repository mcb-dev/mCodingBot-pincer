#! /usr/bin/env bash
set -euo pipefail

if [[ -d .git ]]; then
    git pull

fi

$1 -m venv venv
$1 venv/bin/activate
$1 -m pip install --upgrade pip
$1 -m pip install --upgrade -r requirements.txt
$1 -m pip install -e .

$1 -m mcoding_bot
