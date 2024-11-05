from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager
from accounts.fields import LowercaseEmailField


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = LowercaseEmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "accounts"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        return full_name if full_name else self.email
