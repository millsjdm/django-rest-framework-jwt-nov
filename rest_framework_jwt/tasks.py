# Standard Library
import logging

# Third-Party
from django_rq import job
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.crypto import get_random_string

from rest_framework_jwt.settings import api_settings
from django.forms.models import model_to_dict


log = logging.getLogger(__name__)

def get_auth0():
    """
    Retrieve instantiated auth0 client.

    This also uses the cache so we're not re-instantiating for every update.
    """
    auth0_api_access_token = cache.get('auth0_api_access_token')
    if not auth0_api_access_token:
        client = GetToken(
            api_settings.AUTH0_DOMAIN,
        )
        response = client.client_credentials(
            api_settings.AUTH0_CLIENT_ID,
            api_settings.AUTH0_CLIENT_SECRET,
            api_settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'auth0_api_access_token',
            response['access_token'],
            timeout=response['expires_in'],
        )
        auth0_api_access_token = response['access_token']
    auth0 = Auth0(
        api_settings.AUTH0_DOMAIN,
        auth0_api_access_token,
    )
    return auth0


def get_or_create_account_from_email(email):
    auth0 = get_auth0()
    results = auth0.users_by_email.search_users_by_email(email)
    if results:
        account = results[0]
        created = False
    else:
        password = get_random_string()
        payload = {
            'connection': api_settings.AUTH0_CONNECTION,
            'email': email,
            'email_verified': True,
            'password': password,
        }
        account = auth0.users.create(payload)
        created = True
    return account, created


@job('low')
def update_account_from_user(user):
    auth0 = get_auth0()
    payload = model_to_dict(
        user,
        fields=[
            'email',
            'name',
            'first_name',
            'last_name',
            'app_metadata',
            'user_metadata',
        ]
    )
    # Re-write payload to conform to Auth0
    if user.image_url:
        payload['picture'] = user.image_url
    payload['given_name'] = payload.pop('first_name')
    payload['family_name'] = payload.pop('last_name')
    return auth0.users.update(user.username, payload)


@job('low')
def delete_account_from_user(user):
    auth0 = get_auth0()
    return auth0.users.delete(user.username)

@job('low')
def add_account_roles_from_user_pk_set(user, role, pk_set):
    auth0 = get_auth0()
    roles_raw = role.objects.filter(id__in=pk_set)
    roles = [str(i.rolename) for i in roles_raw]
    return auth0.users.add_roles(user.username, roles)

@job('low')
def remove_account_roles_from_user_pk_set(user, role, pk_set):
    auth0 = get_auth0()
    roles_raw = role.objects.filter(id__in=pk_set)
    roles = [str(i.rolename) for i in roles_raw]
    return auth0.users.remove_roles(user.username, roles)

