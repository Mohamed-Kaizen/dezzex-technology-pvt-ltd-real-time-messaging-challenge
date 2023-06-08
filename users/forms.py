"""Collection of forms."""

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from .validators import (
    validate_confusables,
    validate_confusables_email,
    validate_reserved_name,
)


class CustomUserCreationForm(UserCreationForm):
    """Custom form for users creation form in admin page."""

    class Meta:
        """Meta data."""

        model = CustomUser
        fields = ("username", "password")

    def clean_username(self: "CustomUserCreationForm") -> str:
        """Extra validation for username."""
        username = self.data.get("username")

        validate_confusables(value=username, exception_class=ValidationError)

        validate_reserved_name(value=username, exception_class=ValidationError)

        return self.cleaned_data["username"]

    def clean_email(self: "CustomUserCreationForm") -> str:
        """Extra validation for email."""
        email = self.data.get("email")

        local_part, domain = email.split("@")
        validate_confusables_email(
            local_part=local_part,
            domain=domain,
            exception_class=ValidationError,
        )

        validate_reserved_name(value=local_part, exception_class=ValidationError)

        return self.cleaned_data["email"]


class CustomUserChangeForm(UserChangeForm):
    """Custom form for users change form in admin page."""

    class Meta:
        """Meta data."""

        model = CustomUser
        fields = ("username", "email")

    def clean_username(self: "CustomUserChangeForm") -> str:
        """Extra validation for username."""
        username = self.data.get("username")

        validate_confusables(value=username, exception_class=ValidationError)

        validate_reserved_name(value=username, exception_class=ValidationError)

        return self.cleaned_data["username"]

    def clean_email(self: "CustomUserChangeForm") -> str:
        """Extra validation for email."""
        email = self.data.get("email")

        local_part, domain = email.split("@")

        validate_confusables_email(
            local_part=local_part,
            domain=domain,
            exception_class=ValidationError,
        )

        validate_reserved_name(value=local_part, exception_class=ValidationError)

        return self.cleaned_data["email"]
