#!/usr/bin/env bash
# run.sh
# Quick way to start the Divar car scraper
# Usage: ./run.sh

set -euo pipefail 

echo "======================================"
echo "  Divar Car Scraper  (personal project)"
echo "======================================"
echo ""

# Optional: if you later create a virtual environment, uncomment this:

# if [ -d "venv" ]; then
#     echo "Activating virtual environment..."
#     source venv/bin/activate
# fi

echo "Changing to source directory..."
cd src || { echo "Error: src/ folder not found"; exit 1; }

echo "Running main.py ..."
echo ""

python3 main.py

echo ""
echo "======================================"
echo "Finished."
echo "======================================"