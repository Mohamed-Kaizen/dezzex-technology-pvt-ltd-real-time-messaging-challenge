#!/usr/bin/env python
"""Django manage."""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "dezzex_technology_pvt_ltd_real_time_messaging_challenge.settings",
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        msg = """Couldn't import Django. Are you sure it's
              installed and available on your PYTHONPATH environment variable?
              Did you forget to activate a virtual environment?"""
        raise ImportError(
            msg,
        ) from exc
    execute_from_command_line(sys.argv)
