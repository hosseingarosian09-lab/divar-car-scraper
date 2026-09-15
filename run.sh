#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

echo
echo "==============================================="
echo "        Divar Car Scraper - Linux Run"
echo "==============================================="
echo

if [ ! -f "config.json" ]; then
    echo "Setup has not been completed yet."
    echo "Run ./setup.sh first."
    exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "Project dependencies are not set up yet."
    echo "Run ./setup.sh first."
    exit 1
fi

if [ ! -f "src/main.py" ]; then
    echo "ERROR: src/main.py was not found."
    echo "Make sure run.sh is in the project root."
    exit 1
fi

.venv/bin/python src/main.py
exit_code=$?

echo
if [ "$exit_code" -eq 0 ]; then
    echo "Scraper finished."
else
    echo "Scraper stopped with an error. Exit code: $exit_code"
fi

exit "$exit_code"
