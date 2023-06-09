"""Collection of model."""
import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    """Reference to room model."""

    id = models.UUIDField(  # noqa: A003
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
        primary_key=True,
    )

    class Meta:
        """Meta data."""

        verbose_name = _("room")
        verbose_name_plural = _("rooms")

    def __str__(self: "Room") -> str:
        """It returns readable name for the model."""
        return f"{self.id}"


class Participant(models.Model):
    """Reference to participant model."""

    id = models.UUIDField(  # noqa: A003
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
        primary_key=True,
    )

    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="participants",
        db_index=True,
    )

    room = models.ForeignKey(
        Room,
        verbose_name=_("room"),
        on_delete=models.CASCADE,
        related_name="participants",
        db_index=True,
    )

    class Meta:
        """Meta data."""

        verbose_name = _("participant")
        verbose_name_plural = _("participants")

    def __str__(self: "Participant") -> str:
        """It returns readable name for the model."""
        return f"{self.user} in {self.room}"


class Message(models.Model):
    """Reference to message model."""

    id = models.UUIDField(  # noqa: A003
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
        primary_key=True,
    )

    room = models.ForeignKey(
        Room,
        verbose_name=_("room"),
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True,
    )

    sender = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("sender"),
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True,
    )

    content = models.TextField(verbose_name=_("content"))

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)

    class Meta:
        """Meta data."""

        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self: "Message") -> str:
        """It returns readable name for the model."""
        return f"{self.sender.username} in {self.room.id}"


@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs: dict) -> None:  # noqa
    """Send message to room group."""
    if created:
        from .schema import MessageSchema

        message = MessageSchema.from_orm(instance)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"chat_{instance.room.id}",
            {
                "type": "chat_message",
                "message": message.json(),
            },
        )
