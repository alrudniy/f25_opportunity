#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # If the 'test' command is being run, use the test settings module.
    # This ensures that an in-memory SQLite database is used,
    # avoiding potential PostgreSQL permission issues for creating test databases.
    if 'test' in sys.argv:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opportunity_app.settings_test')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opportunity_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
