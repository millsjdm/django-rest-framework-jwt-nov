# Django
from django.contrib.auth.models import BaseUserManager

from .utils import get_or_create_account_from_email

class UserManager(BaseUserManager):
    def get_or_create_user_from_email(self, email):
        try:
            user = self.get(email=email)
            created = False
        except self.model.DoesNotExist:
            created = True
            account, _ = get_or_create_account_from_email(email)
            user = self.create_user(account['user_id'], email=email)
        return user, created


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
        email = payload.get('email', None)
        name = payload.get('name', "Unknown")
        first_name = payload.get('given_name', "Unknown")
        last_name = payload.get('family_name', "Unknown")
        email_verified = payload.get('email_verified', False)
        image = payload.get('picture', "")
        app_metadata = payload.get('https://login.barberscore.com/app_metadata', {})
        user_metadata = payload.get('https://login.barberscore.com/user_metadata', {})
        roles = payload.get('https://login.barberscore.com/roles', [])

        # Transform

        # Load
        defaults = {
            'email': email,
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
            'email_verified': email_verified,
            'image': image,
            'app_metadata': app_metadata,
            'user_metadata': user_metadata,
            'roles': roles,
        }
        user, created = self.update_or_create(
            username=username,
            defaults=defaults,
        )
        if created:
            user.set_unusable_password()
            user.save(using=self._db)
        return user, created
