# Standard Library
import uuid

# Django
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

# First-Party
from .managers import UserManager
from .fields import UploadPath
from .validators import validate_punctuation

class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        editable=True,
    )

    name = models.CharField(
        max_length=100,
        editable=True,
        validators=[
            validate_punctuation,
        ],
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=True,
        validators=[
            validate_punctuation,
        ],
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=True,
        validators=[
            validate_punctuation,
        ],
    )

    email_verified = models.BooleanField(
        default=False,
    )

    image = models.ImageField(
        upload_to=UploadPath('image'),
        max_length=255,
        blank=True,
        default="",
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

    roles = models.ManyToManyField(
        'rest_framework_jwt.role',
        blank=True,
        related_name="roles",
    )

    objects = UserManager()

    @property
    def is_superuser(self):
        return bool(self.is_staff)

    @property
    def image_name(self):
        return self.image.name

    @property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return ''

    # User Internals
    class JSONAPIMeta:
        resource_name = "user"

    def __str__(self):
        return str(self.email)

    def clean(self):
        pass

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Role(models.Model):
    """
    Inheirts from core Group
    """
    id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        unique=True,
        editable=True,
    )
    description = models.TextField(
        blank=True,
        default='',
    )

    def __str__(self):
        return self.name