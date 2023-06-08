"""Collection of test for users views."""

import pytest
from django.test import Client
from ninja_jwt.tokens import RefreshToken

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


@pytest.fixture()
def get_or_create_token(django_user_model: CustomUser, user_creation_data: dict) -> str:
    """A fixture for token."""
    user = django_user_model.objects.create_user(
        **user_creation_data,
    )

    token = RefreshToken.for_user(user)

    return token.access_token


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


@pytest.mark.django_db()
def test_unauthorized_user_profile(client: Client) -> None:
    """Test for unauthorized user.

    This test will fail because we are not sending any token.
    """
    response = client.get("/api/users/")

    data = response.json()

    assert data.get("detail") == "Unauthorized"
    assert response.status_code == 401  # noqa


@pytest.mark.django_db()
def test_authorized_user_profile(
    client: Client,
    get_or_create_token: str,
    user_creation_data: dict,
) -> None:
    """Test for authorized user.

    This test will pass because we are sending a token.
    """
    response = client.get(
        "/api/users/",
        HTTP_AUTHORIZATION=f"Bearer {get_or_create_token}",
    )

    data = response.json()

    assert data.get("user") == user_creation_data.get("username")

    assert data.get("email") == user_creation_data.get("email")

    assert data.get("full_name") == user_creation_data.get("full_name")

    assert response.status_code == 200  # noqa
