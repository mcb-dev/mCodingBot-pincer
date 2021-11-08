#! /usr/bin/env bash
set -euo pipefail

if [[ -d .git ]]; then
    git pull

fi

python -m venv venv
venv/bin/pip install -U --target venv/lib/python3.8/site-packages/ -r requirements.txt

venv/bin/pip install -e .
venv/bin/python mcoding_bot/__main__.py
