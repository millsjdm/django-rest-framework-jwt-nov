from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilterset(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': [
                'exact',
            ],
        }
