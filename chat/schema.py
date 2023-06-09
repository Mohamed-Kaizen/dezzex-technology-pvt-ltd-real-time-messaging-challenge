"""Schemas for chat app."""
from uuid import UUID

from ninja import ModelSchema
from pydantic import BaseModel

from .models import Message


class CreateMessageSchema(BaseModel):
    """Create message schema."""

    content: str

    recipient_id: UUID


class CreateMessageRespondSchema(BaseModel):
    """Create message response schema."""

    message: str


class MessageSchema(ModelSchema):
    """Message schema."""

    class Config:
        """Message schema config."""

        model = Message
        model_exclude = ("room",)
