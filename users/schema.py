"""Schemas for user app."""
from ninja import ModelSchema
from pydantic import EmailStr, validator

from .models import CustomUser
from .validators import (
    validate_confusables,
    validate_confusables_email,
    validate_reserved_name,
)


class UserSchema(ModelSchema):
    """User schema."""

    username: str

    email: EmailStr

    @validator("email")
    def validate_email(cls: "UserSchema", value: str) -> str:  # noqa
        """Validate email."""
        if CustomUser.objects.filter(email=value).exists():
            msg = "Email already exists"
            raise ValueError(msg)

        local_part, domain = value.split("@")

        validate_confusables_email(
            local_part=local_part,
            domain=domain,
            exception_class=ValueError,
        )

        validate_reserved_name(value=local_part, exception_class=ValueError)

        validate_reserved_name(value=domain, exception_class=ValueError)
        return value

    @validator("username")
    def validate_username(cls: "UserSchema", value: str) -> str:  # noqa
        """Validate username."""
        if CustomUser.objects.filter(username=value).exists():
            msg = "Username already exists"
            raise ValueError(msg)

        validate_confusables(value=value, exception_class=ValueError)

        validate_reserved_name(value=value, exception_class=ValueError)

        return value

    class Config:
        """User schema config."""

        model = CustomUser
        model_fields = ["username", "email", "full_name", "password"]

