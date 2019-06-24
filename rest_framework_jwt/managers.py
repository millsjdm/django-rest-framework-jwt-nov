
# Standard Library
import json
import logging
import uuid
import maya

# Third-Party
import django_rq
from algoliasearch_django.decorators import disable_auto_indexing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import CharField
from django.db.models import F
from django.db.models import Manager
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.utils.timezone import localdate
from django.utils.timezone import now

# First-Party


class UserManager(BaseUserManager):
    def create_user(self, username, **kwargs):
        user = self.model(
            username=username,
            **kwargs
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            is_staff=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_or_create_user_from_payload(self, username, payload):
        # Extract
        print(payload)
        name = payload.get('name', "Unknown")
        given_name = payload.get('given_name', "Unknown")
        family_name = payload.get('family_name', "Unknown")
        email = payload.get('email', None)
        email_verified = payload.get('email_verified', False)
        image = payload.get('picture', "")
        app_metadata = payload.get('app_metadata', {})
        user_metadata = payload.get('user_metadata', {})

        # Transform

        # Load
        defaults = {
            'name': name,
            'given_name': given_name,
            'family_name': family_name,
            'email': email,
            'email_verified': email_verified,
            'image': image,
            'app_metadata': app_metadata,
            'user_metadata': user_metadata,
        }
        user, created = self.update_or_create(
            username=username,
            defaults=defaults,
        )
        if created:
            user.set_unusable_password()
            user.save(using=self._db)
        return user, created
