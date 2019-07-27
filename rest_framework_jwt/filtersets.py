from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Role


class UserFilterset(FilterSet):
    class Meta:
        model = User
        fields = {
            'id': [
                'exact',
            ],
            'username': [
                'exact',
            ],
            'name': [
                'contains',
            ],
        }


class RoleFilterset(FilterSet):
    class Meta:
        model = Role
        fields = {
            'id': [
                'exact',
            ],
            'rolename': [
                'exact',
            ],
            'name': [
                'exact',
            ],
        }
