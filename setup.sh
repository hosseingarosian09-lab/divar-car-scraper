#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo
echo "==============================================="
echo "       Divar Car Scraper - Linux Setup"
echo "==============================================="
echo

as_root() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        echo "ERROR: Administrator privileges are required to install system packages."
        echo "Run the command as root or install sudo, then try again."
        exit 1
    fi
}

python_ok() {
    command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1
}

install_python() {
    echo "Python 3.10 or newer was not found."
    echo "Trying to install Python with the system package manager..."
    echo

    if command -v apt-get >/dev/null 2>&1; then
        as_root apt-get update
        as_root apt-get install -y python3 python3-venv python3-pip
    elif command -v dnf >/dev/null 2>&1; then
        as_root dnf install -y python3 python3-pip
    elif command -v pacman >/dev/null 2>&1; then
        as_root pacman -Sy --noconfirm python python-pip
    elif command -v zypper >/dev/null 2>&1; then
        as_root zypper --non-interactive install python3 python3-pip python3-virtualenv
    else
        echo "ERROR: No supported package manager was found."
        echo "Install Python 3.10+ manually, then run ./setup.sh again."
        exit 1
    fi
}

install_venv_support() {
    if command -v apt-get >/dev/null 2>&1; then
        as_root apt-get update
        as_root apt-get install -y python3-venv
    else
        echo "ERROR: Python is installed, but it could not create a virtual environment."
        echo "Install your distribution's Python venv/virtualenv package and run ./setup.sh again."
        exit 1
    fi
}

if ! python_ok; then
    install_python
fi

if ! python_ok; then
    echo
    echo "ERROR: The available Python version is older than Python 3.10."
    echo "Install Python 3.10 or newer and run ./setup.sh again."
    exit 1
fi

echo "Using Python:"
python3 --version

echo
echo "Creating the project virtual environment..."
if [ ! -x ".venv/bin/python" ]; then
    if ! python3 -m venv .venv; then
        rm -rf .venv
        install_venv_support
        python3 -m venv .venv
    fi
fi

echo
echo "Preparing pip..."
.venv/bin/python -m pip install --upgrade pip

echo
echo "Installing project requirements..."
.venv/bin/python -m pip install -r requirements.txt

while true; do
    echo
    echo "Choose the output format:"
    echo "  1. CSV"
    echo "  2. JSON"
    read -r -p "Enter 1 or 2: " format_choice

    case "$format_choice" in
        1)
            save_format="csv"
            break
            ;;
        2)
            save_format="json"
            break
            ;;
        *)
            echo "Invalid choice. Please enter 1 or 2."
            ;;
    esac
done

printf '{"format":"%s"}\n' "$save_format" > config.json

echo
echo "==============================================="
echo "Setup completed successfully."
echo "Output format: $save_format"
echo
echo "Run the scraper with: ./run.sh"
echo "==============================================="
echo
