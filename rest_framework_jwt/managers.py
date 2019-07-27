# Django
from django.contrib.auth.models import BaseUserManager

# from .utils import get_auth0
from django.utils.crypto import get_random_string
# from .tasks import get_username_from_email

class UserManager(BaseUserManager):
    def create_user(self, username, email, **kwargs):
        user = self.model(
            username=username,
            email=email,
            **kwargs
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        user = self.model(
            username=username,
            email=email,
            is_staff=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
