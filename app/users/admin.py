from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Value, F
from django.db.models.functions import Concat

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_filter = ["is_staff", "is_superuser", "is_active"]
    search_fields = [
        "first_name_last_name",  # see get_queryset
        "first_name",
        "last_name",
        "email",
    ]
    list_display = [
        "full_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    ordering = ["-id"]
    readonly_fields = ["created_at", "updated_at", "last_login"]
    actions = ["deactivate_action", "activate_action"]

    add_form = UserCreationForm
    form = UserChangeForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    )
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal",
            {
                "fields": [
                    "first_name",
                    "last_name",
                ],
            },
        ),
        (
            "Moderation",
            {"fields": ["created_at", "updated_at", "last_login"]},
        ),
        (
            "Authorization",
            {
                "classes": ["collapse"],
                "fields": [
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ],
            },
        ),
    ]

    def get_redirect_to_previous_page(self, request):
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        return redirect(reverse("admin:users_user_changelist"))

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                first_name_last_name=Concat(F("first_name"), Value(" "), F("last_name"))
            )
        )

    def has_delete_permission(self, *args, **kwargs):
        return False

    def deactivate_action(self, request, queryset):
        count = queryset.active().deactivate(request.user.id)
        self.message_user(request, f"Deactivated {count} users", level=messages.SUCCESS)
        return self.get_redirect_to_previous_page(request)

    deactivate_action.short_description = "Deactivate selected"

    def activate_action(self, request, queryset):
        count = queryset.inactive().activate(request.user.id)
        self.message_user(request, f"Activated {count} users", level=messages.SUCCESS)
        return self.get_redirect_to_previous_page(request)

    activate_action.short_description = "Activate selected"
