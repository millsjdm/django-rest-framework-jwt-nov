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
            'name': [
                'contains',
                'exact',
            ],
            'email': [
                'exact',
            ],
        }


class RoleFilterset(FilterSet):
    class Meta:
        model = Role
        fields = {
            'id': [
                'exact',
            ],
            'name': [
                'exact',
            ],
        }
