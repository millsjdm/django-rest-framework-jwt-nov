# Django
from django.contrib.auth.models import BaseUserManager

from .utils import get_auth0
from django.utils.crypto import get_random_string

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

    def get_or_create(self, *args, **kwargs):
        """
        Customized Auth0 get_or_create

        This gets or creates an Auth0 account prior to calling super for the User
        """
        email = kwargs.get('email', None)
        role = kwargs.get('role', None)

        auth0 = get_auth0()
        results = auth0.users_by_email.search_users_by_email(email)
        if results:
            account = results[0]
        else:
            password = get_random_string()
            payload = {
                'connection': 'Default',
                'email': kwargs['email'],
                'email_verified': True,
                'password': password,
            }
            account = auth0.users.create(payload)
        username = account['user_id']
        if role:
            role_id = auth0.roles.list(name_filter=officer.get_office_display())['roles'][0]['id']
            auth0.users.add_roles(username, [role_id])
        return super().get_or_create(username=username, *args, **kwargs)
