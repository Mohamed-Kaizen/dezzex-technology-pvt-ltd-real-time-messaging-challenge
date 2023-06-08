"""WSGI config for Dezzex Technology Pvt Ltd real-time messaging challenge project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "dezzex_technology_pvt_ltd_real_time_messaging_challenge.settings",
)

application = get_wsgi_application()
