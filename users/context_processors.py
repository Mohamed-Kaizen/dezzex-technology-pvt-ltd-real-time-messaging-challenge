"""Collection of template processor."""
from typing import Any

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


def from_settings(request: WSGIRequest) -> dict[str, Any]:
    """Custom template processor to show current env."""
    return {
        "ENVIRONMENT_NAME": settings.ENVIRONMENT_NAME,
        "ENVIRONMENT_COLOR": settings.ENVIRONMENT_COLOR,
    }
