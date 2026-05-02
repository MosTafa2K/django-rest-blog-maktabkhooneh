from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profile, User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
        "is_verified",
    ]
    list_filter = ["is_staff", "is_active", "is_verified"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
        (
            "Groups and Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (None, {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": {
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                },
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
