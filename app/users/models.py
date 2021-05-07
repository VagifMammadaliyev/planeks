from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    @transaction.atomic
    def _toggle_active_field(self, is_active, admin_id):
        if admin_id:
            change_message = (
                "Activated this user." if is_active else "Deactivated this user."
            )
            log_entries = []
            user_ids = self.values_list("pk", flat=True)
            user_ct = User.get_content_type()
            for user_id in user_ids:
                log_entries.append(
                    LogEntry(
                        user_id=admin_id,
                        content_type_id=user_ct.id,
                        object_id=str(user_id),
                        object_repr=f"User with id={user_id}",
                        action_flag=CHANGE,
                        change_message=change_message,
                    )
                )
            LogEntry.objects.bulk_create(log_entries)

        count = self.update(is_active=is_active)
        return count

    def deactivate(self, admin_id=None):
        return self._toggle_active_field(is_active=False, admin_id=admin_id)

    def activate(self, admin_id=None):
        return self._toggle_active_field(is_active=True, admin_id=admin_id)


class UserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, email=None, password=None, is_active=True, commit=True):
        user = self.model(email=email, is_active=is_active)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, commit=True):
        user = self.create_user(email=email, password=password, commit=False)
        user.is_superuser = True
        user.is_staff = True
        if commit:
            user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    DEFAULT_FULL_NAME = "Unknown"

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self):
        return f"{self.email} - [{self.full_name}]"

    @property
    def full_name(self):
        first_name = self.first_name and self.first_name.strip()
        last_name = self.last_name and self.last_name.strip()

        if first_name or last_name:
            return f"{first_name} {last_name}".strip()


        return self.DEFAULT_FULL_NAME

    @classmethod
    def get_content_type(cls):
        return ContentType.objects.get_for_model(cls)
