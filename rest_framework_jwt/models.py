
# Standard Library
import logging
import uuid

# Django
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.postgres.fields import JSONField

# First-Party
from .fields import LowerEmailField
from .fields import ImageUploadPath
from .managers import UserManager


log = logging.getLogger(__name__)


# class User(AbstractBaseUser):
#     USERNAME_FIELD = settings.USERNAME_FIELD
#     REQUIRED_FIELDS = settings.REQUIRED_FIELDS

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#     )

#     username = models.CharField(
#         max_length=100,
#         unique=True,
#         editable=True,
#     )

#     name = models.CharField(
#         max_length=100,
#         blank=True,
#         default='',
#         editable=True,
#     )

#     given_name = models.CharField(
#         max_length=100,
#         blank=True,
#         default='',
#         editable=True,
#     )

#     family_name = models.CharField(
#         max_length=100,
#         blank=True,
#         default='',
#         editable=True,
#     )

#     email = LowerEmailField(
#         help_text="""
#             The contact email of the resource.""",
#         blank=True,
#         null=True,
#     )

#     email_verified = models.BooleanField(
#         default=False,
#     )

#     image = models.ImageField(
#         upload_to=ImageUploadPath(),
#         max_length=255,
#         null=True,
#         blank=True,
#     )

#     app_metadata = JSONField(
#         null=True,
#         blank=True,
#     )

#     user_metadata = JSONField(
#         null=True,
#         blank=True,
#     )

#     is_active = models.BooleanField(
#         default=True,
#     )

#     is_staff = models.BooleanField(
#         default=False,
#     )

#     created = models.DateTimeField(
#         auto_now_add=True,
#         editable=False,
#     )

#     modified = models.DateTimeField(
#         auto_now=True,
#         editable=False,
#     )

#     objects = UserManager()

#     @property
#     def is_superuser(self):
#         return bool(self.is_staff)


#     # User Internals
#     class JSONAPIMeta:
#         resource_name = "user"

#     def __str__(self):
#         return str(self.name)

#     def clean(self):
#         pass

#     def has_perm(self, perm, obj=None):
#         return self.is_staff

#     def has_module_perms(self, app_label):
#         return self.is_staff
from django.utils.functional import cached_property
from dry_rest_permissions.generics import allow_staff_or_superuser
from auth0.v3.exceptions import Auth0Error
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from django.apps import apps

# Django
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property


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

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
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

    person = models.OneToOneField(
        'bhs.person',
        related_name='user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    is_convention_manager = models.BooleanField(
        default=False,
    )

    is_session_manager = models.BooleanField(
        default=False,
    )

    is_round_manager = models.BooleanField(
        default=False,
    )

    is_scoring_manager = models.BooleanField(
        default=False,
    )

    is_group_manager = models.BooleanField(
        default=False,
    )

    is_person_manager = models.BooleanField(
        default=False,
    )

    is_award_manager = models.BooleanField(
        default=False,
    )

    is_officer_manager = models.BooleanField(
        default=False,
    )

    is_chart_manager = models.BooleanField(
        default=False,
    )

    is_assignment_manager = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    @cached_property
    def is_mc(self):
        """Proxy status."""
        return bool(getattr(getattr(self, 'person'), 'mc_pk', None))

    @cached_property
    def is_active(self):
        """Proxy status."""
        # if self.is_staff:
        #     return True
        # if self.person:
        #     return bool(self.person.status > 0)
        return True

    @cached_property
    def is_superuser(self):
        return bool(self.is_staff)


    class Meta:
        db_table='api_user'

    class JSONAPIMeta:
        resource_name = "user"

    # User Internals
    def __str__(self):
        if getattr(self, 'person'):
            return self.person.common_name
        return self.username

    def clean(self):
        pass

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # User Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if request.user == self:
            return True
        return False
