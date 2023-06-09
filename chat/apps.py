"""Core app for chat app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatConfig(AppConfig):
    """Class representing a Django application and its configuration."""

    default_auto_field = "django.db.models.BigAutoField"

    name = "chat"
    verbose_name = _("Chats")
