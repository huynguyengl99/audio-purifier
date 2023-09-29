#!/usr/bin/env bash

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ "$1" == "--fix" ]; then
  ruff check . --fix && black ./audio_purifier && toml-sort pyproject.toml
else
  ruff check . && black ./audio_purifier --check && toml-sort pyproject.toml --check
fi
