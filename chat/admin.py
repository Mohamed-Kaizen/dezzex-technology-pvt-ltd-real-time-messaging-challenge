"""Admin module for chat app."""
from django.contrib import admin

from .models import Message, Participant, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Configure the room model in admin page."""

    list_display = ("id",)

    search_fields = ("id", "participants")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Configure the participant model in admin page."""

    list_display = (
        "id",
        "user",
        "room",
    )

    search_fields = (
        "user",
        "room",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Configure the message model in admin page."""

    list_display = (
        "id",
        "room",
        "sender",
        "created_at",
        "updated_at",
    )

    list_filter = ("updated_at",)

    date_hierarchy = "created_at"

    search_fields = ("id", "room", "sender", "content")
