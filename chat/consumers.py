"""The consumers module for chat app."""
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError
from django.db.models import Q
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.exceptions import InvalidToken

from chat.models import Room
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat consumer."""

    async def connect(self: "ChatConsumer") -> None:
        """Join room group."""
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        await self.accept()

    async def disconnect(self: "ChatConsumer", close_code=None) -> None:  # noqa
        """Leave room group."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()

    async def receive(self: "ChatConsumer", **kwargs: dict) -> None:
        """Receive message from WebSocket."""
        data = json.loads(kwargs.get("text_data"))

        token = data.get("token")

        if not token:
            await self.send(text_data=json.dumps({"error": "Invalid token"}))

        jwt = JWTBaseAuthentication()

        try:
            validated_token = jwt.get_validated_token(token)
            user = await self.get_user(validated_token)

            room = await self.get_room(user, self.room_id)

            if not room:
                await self.send(text_data=json.dumps({"error": "Room not found"}))

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        except InvalidToken as e:
            await self.send(text_data=json.dumps({"error": e.detail}))

        except ValidationError as e:
            await self.send(text_data=json.dumps({"error": e.messages}))
        except Room.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Room does not exist"}))

    async def chat_message(self: "ChatConsumer", event: dict) -> None:
        """It sends message to the room group."""
        message = event["message"]
        await self.send(text_data=message)

    @database_sync_to_async
    def get_user(self: "ChatConsumer", token: str) -> CustomUser:
        """It returns user object if token is valid."""
        jwt = JWTBaseAuthentication()

        return jwt.get_user(token)

    @database_sync_to_async
    def get_room(self: "ChatConsumer", user: CustomUser, room_id: str) -> Room:
        """It returns room object if user is participant of the room."""
        return Room.objects.filter(
            Q(participants__user__id=user.id) & Q(id=room_id),
        ).first()
