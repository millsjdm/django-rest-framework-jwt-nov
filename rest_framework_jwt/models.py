# Standard Library
import uuid

# Django
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.postgres.fields import JSONField

# First-Party
from .managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=True,
    )

    given_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=True,
    )

    family_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=True,
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
    )

    email_verified = models.BooleanField(
        default=False,
    )

    image = models.ImageField(
        max_length=255,
        null=True,
        blank=True,
    )

    app_metadata = JSONField(
        null=True,
        blank=True,
    )

    user_metadata = JSONField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    objects = UserManager()

    @property
    def is_superuser(self):
        return bool(self.is_staff)


    # User Internals
    class JSONAPIMeta:
        resource_name = "user"

    def __str__(self):
        return str(self.name)

    def clean(self):
        pass

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
