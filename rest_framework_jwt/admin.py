# Third-Party

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import Group as AuthGroup
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget

# Local
from .forms import AccountUserCreationForm

from .models import User
from .models import Role


admin.site.site_header = 'Admin Backend'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = AccountUserCreationForm
    list_display = [
        'id',
        'name',
        'email',
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'roles',
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'first_name', 'last_name', ),
        }),
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'name',
                'email',
                'first_name',
                'last_name',
                'user_metadata',
                'roles',
                'image',
                # 'app_metadata',
                'created',
                'modified',
            )
        }),
    )
    search_fields = [
        'email',
        'name',
        'first_name',
        'last_name',
    ]
    ordering = (
        'last_name',
        'first_name',
    )
    filter_horizontal = ()
    readonly_fields = [
        'id',
        'created',
        'modified',
    ]
    autocomplete_fields = [
        'roles',
    ]
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
    ]
    list_filter = [
    ]
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'name',
                'description',
            )
        }),
    )
    search_fields = [
        'name',
    ]
    ordering = (
        'id',
        'name',
    )
    readonly_fields = [
        'id',
    ]


admin.site.unregister(AuthGroup)
