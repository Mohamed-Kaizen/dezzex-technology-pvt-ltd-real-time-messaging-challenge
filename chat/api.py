"""API routes for users app."""
from uuid import UUID

from django.db.models import Q
from ninja import Router
from ninja.errors import Http404, HttpError
from ninja_jwt.authentication import JWTAuth

from users.models import CustomUser  # noqa

from .models import Message, Participant, Room
from .schema import CreateMessageRespondSchema, CreateMessageSchema, MessageSchema

router = Router()


@router.post("/create-message", auth=JWTAuth(), response=CreateMessageRespondSchema)
def create_message(request, payload: CreateMessageSchema) -> dict:  # noqa
    """Create a new message."""
    user: CustomUser = request.auth

    room = Room.objects.filter(participants__user__id=payload.recipient_id).filter(
        participants__user__id=user.id,
    )

    if not room.exists():
        try:
            room = Room.objects.create()
            Participant.objects.create(user=user, room=room)
            Participant.objects.create(user_id=payload.recipient_id, room=room)

            Message.objects.create(content=payload.content, sender=user, room=room)
        except Exception as e:
            raise HttpError(400, "Error creating room") from e
    else:
        Message.objects.create(content=payload.content, sender=user, room=room.first())

    return {"message": "Message sent"}


@router.get("/{room_id}", auth=JWTAuth(), response=list[MessageSchema])
def get_messages(request, room_id: UUID) -> Message:  # noqa
    """Get messages for a room."""
    user: CustomUser = request.auth

    if room := Room.objects.filter(
        Q(participants__user__id=user.id) & Q(id=room_id),
    ).first():
        return Message.objects.filter(room=room).order_by("-created_at")
    raise Http404("Room not found")  # noqa
