"""Collection of test for users views."""

import pytest
from django.test import Client

from users.models import CustomUser


@pytest.fixture()
def user_creation_data() -> dict:
    """A fixture for user creation."""
    return {
        "username": "mohamed",
        "password": "123456789test",
        "email": "test@test.com",
        "full_name": "Mohamed",
    }


@pytest.mark.django_db()
def test_sign_up(client: Client, user_creation_data: dict) -> None:
    """Test for sign up endpoint."""
    response = client.post(
        "/api/users/",
        user_creation_data,
        content_type="application/json",
    )

    data = response.json()

    assert data.get("refresh") is not None

    assert data.get("access") is not None

    assert response.status_code == 200  # noqa


@pytest.mark.django_db()
def test_sign_in(
    client: Client,
    django_user_model: CustomUser,
    user_creation_data: dict,
) -> None:
    """Test for sign in endpoint."""
    django_user_model.objects.create_user(**user_creation_data)

    response = client.post(
        "/api/token/pair",
        user_creation_data,
        content_type="application/json",
    )
    data = response.json()

    assert data.get("refresh") is not None

    assert data.get("access") is not None

    assert data.get("username") is not None

    assert response.status_code == 200  # noqa
