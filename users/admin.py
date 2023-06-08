"""Admin module for users app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Configure the users app in admin page."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (_("Permissions"), {"fields": ("is_superuser", "is_staff")}),
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "classes": ("collapse",),
                "fields": (
                    "full_name",
                    "email",
                    "picture",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"classes": ("collapse",), "fields": ("last_login", "date_joined")},
        ),
    )

    list_display = (
        "username",
        "email",
        "is_active",
    )

    list_filter = ("last_login",)

    date_hierarchy = "date_joined"


admin.site.site_title = _(
    "Dezzex Technology Pvt Ltd real-time messaging challenge site admin",
)
admin.site.site_header = _(
    "Dezzex Technology Pvt Ltd real-time messaging challenge Dashboard",
)
admin.site.index_title = _(
    "Welcome to Dezzex Technology Pvt Ltd real-time messaging challenge",
)
