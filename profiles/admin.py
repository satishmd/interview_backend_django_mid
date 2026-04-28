from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile

    list_display = ("email", "is_staff", "is_active", "is_admin")
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "avatar")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_admin", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2","avatar", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)