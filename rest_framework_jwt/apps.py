
# Django
from django.apps import AppConfig


class RestFrameworkJWTConfig(AppConfig):
    name = 'rest_framework_jwt'
    verbose_name = 'Auth0 Authentication'

    def ready(self):
        from .signals import user_pre_save
        from .signals import user_pre_delete
        from .signals import m2m_changed
        return
