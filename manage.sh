#!/bin/sh
# This script activates the virtual environment and runs a Django management command.

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run 'python bootstrap.py' first."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

# Run the Django management command with all passed arguments
exec python manage.py "$@"
