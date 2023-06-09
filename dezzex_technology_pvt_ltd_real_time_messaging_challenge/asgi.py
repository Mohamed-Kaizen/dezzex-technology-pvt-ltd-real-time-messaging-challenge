"""ASGI config for Dezzex Technology Pvt Ltd real-time messaging challenge project."""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application

import chat.routing

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "dezzex_technology_pvt_ltd_real_time_messaging_challenge.settings",
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": OriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)), ["*"],
        ),
    },
)
