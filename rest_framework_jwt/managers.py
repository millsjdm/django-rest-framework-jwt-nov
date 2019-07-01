# Django
from django.contrib.auth.models import BaseUserManager

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
        email = payload.get('email', None)
        name = payload.get('name', "Unknown")
        given_name = payload.get('given_name', "Unknown")
        family_name = payload.get('family_name', "Unknown")
        email_verified = payload.get('email_verified', False)
        image = payload.get('picture', "")
        app_metadata = payload.get('app_metadata', {})
        user_metadata = payload.get('user_metadata', {})

        # Transform

        # Load
        defaults = {
            'email': email,
            'name': name,
            'given_name': given_name,
            'family_name': family_name,
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
