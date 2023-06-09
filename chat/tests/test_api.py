"""Collection of test for users views."""

import pytest
from django.test import Client
from ninja_jwt.tokens import RefreshToken

from chat.models import Room
from users.models import CustomUser


@pytest.fixture()
def user_creation_data() -> list[dict]:
    """A fixture for user creation."""
    return [
        {
            "username": "mohamed",
            "password": "123456789test",
            "email": "test@test.com",
            "full_name": "Mohamed",
        },
        {
            "username": "ahmed",
            "password": "123456789test",
            "email": "ahmed@test.com",
            "full_name": "Ahmed",
        },
        {
            "username": "ali",
            "password": "123456789test",
            "email": "ali@test.com",
            "full_name": "Ali",
        },
    ]


@pytest.mark.django_db()
def test_create_message_for_unauthorized_user(client: Client) -> None:
    """Test for create message endpoint for unauthorized user."""
    response = client.post(
        "/api/chat/create-message",
        {"content": "Hello", "recipient_id": "0e4146de-0c3f-4b72-82d3-047ece742fd9"},
        content_type="application/json",
    )

    data = response.json()

    assert data.get("detail") == "Unauthorized"

    assert response.status_code == 401  # noqa


@pytest.mark.django_db()
def test_create_message_for_authorized_user(
    client: Client,
    django_user_model: CustomUser,
    user_creation_data: list[dict],
) -> None:
    """Test for create message endpoint for authorized user."""
    user1 = django_user_model.objects.create_user(
        **user_creation_data[0],
    )

    user2 = django_user_model.objects.create_user(
        **user_creation_data[1],
    )

    token = RefreshToken.for_user(user1).access_token

    response = client.post(
        "/api/chat/create-message",
        {"content": "Hi", "recipient_id": user2.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )
    data = response.json()

    assert data.get("message") == "Message sent"

    assert response.status_code == 200  # noqa


@pytest.mark.django_db()
def test_get_messages_for_unauthorized_user(client: Client) -> None:
    """Test for get messages endpoint for unauthorized user."""
    response = client.get(
        "/api/chat/0e4146de-0c3f-4b72-82d3-047ece742fd9",
        content_type="application/json",
    )

    data = response.json()

    assert data.get("detail") == "Unauthorized"

    assert response.status_code == 401  # noqa


@pytest.mark.django_db()
def test_get_messages_for_authorized_user(
    client: Client,
    django_user_model: CustomUser,
    user_creation_data: list[dict],
) -> None:
    """Test for get messages endpoint for authorized user."""
    user1 = django_user_model.objects.create_user(
        **user_creation_data[0],
    )

    user2 = django_user_model.objects.create_user(
        **user_creation_data[1],
    )

    user1_token = RefreshToken.for_user(user1).access_token

    user2_token = RefreshToken.for_user(user2).access_token

    client.post(
        "/api/chat/create-message",
        {"content": "Hi", "recipient_id": user2.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user1_token}",
    )

    client.post(
        "/api/chat/create-message",
        {"content": "Hello", "recipient_id": user1.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user2_token}",
    )

    room = (
        Room.objects.filter(participants__user__id=user1.id)
        .filter(
            participants__user__id=user2.id,
        )
        .first()
    )

    assert room is not None

    user1_response = client.get(
        f"/api/chat/{room.id}",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user1_token}",
    )

    user2_response = client.get(
        f"/api/chat/{room.id}",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user2_token}",
    )

    user1_data = user1_response.json()

    user2_data = user2_response.json()

    assert user1_data == user2_data

    assert user1_response.status_code == 200  # noqa

    assert user2_response.status_code == 200  # noqa


@pytest.mark.django_db()
def test_get_messages_for_authorized_user_with_third_user_which_isnt_in_room(
    client: Client,
    django_user_model: CustomUser,
    user_creation_data: list[dict],
) -> None:
    """Test for get messages endpoint for authorized user with third user which isn't in room."""  # noqa
    user1 = django_user_model.objects.create_user(
        **user_creation_data[0],
    )

    user2 = django_user_model.objects.create_user(
        **user_creation_data[1],
    )

    user3 = django_user_model.objects.create_user(
        **user_creation_data[2],
    )

    user1_token = RefreshToken.for_user(user1).access_token

    user2_token = RefreshToken.for_user(user2).access_token

    user3_token = RefreshToken.for_user(user3).access_token

    client.post(
        "/api/chat/create-message",
        {"content": "Hi", "recipient_id": user2.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user1_token}",
    )

    client.post(
        "/api/chat/create-message",
        {"content": "Hello", "recipient_id": user1.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user2_token}",
    )

    room = Room.objects.all().first()

    assert room is not None

    response = client.get(
        f"/api/chat/{room.id}",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user3_token}",
    )

    data = response.json()

    assert data.get("detail") == "Not Found"

    assert response.status_code == 404  # noqa
