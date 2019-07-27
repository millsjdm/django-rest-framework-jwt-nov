
# Django
from django.apps import AppConfig


class RestFrameworkJWTConfig(AppConfig):
    name = 'rest_framework_jwt'
    verbose_name = 'Auth0 Authentication'

    def ready(self):
        from rest_framework_jwt import signals
        return
