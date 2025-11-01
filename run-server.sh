#!/bin/sh
# This script activates the virtual environment and starts the Django development server.

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run 'python bootstrap.py' first."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

# Run the Django development server
# The 'exec' command replaces the shell process with the Django server process.
# "$@" passes along any command-line arguments to manage.py runserver (e.g., a port number)
echo "Starting development server at http://127.0.0.1:8000/"
exec python manage.py runserver "$@"
