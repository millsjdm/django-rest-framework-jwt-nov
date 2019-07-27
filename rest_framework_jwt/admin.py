# Third-Party

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import Group as AuthGroup

# Local
from .forms import AccountUserCreationForm

from .models import User
from .models import Role


admin.site.site_header = 'Admin Backend'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = AccountUserCreationForm
    list_display = [
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
                'username',
                'name',
                'email',
                'first_name',
                'last_name',
                # 'image',
                'roles',
                'app_metadata',
                'user_metadata',
                'created',
                'modified',
            )
        }),
    )
    search_fields = [
        'username',
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
        'username',
        'app_metadata',
        'user_metadata',
        'created',
        'modified',
    ]
    autocomplete_fields = [
        'roles',
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]
    list_filter = [
    ]
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'rolename',
                'description',
            )
        }),
    )
    search_fields = [
        'rolename',
        'name',
    ]
    ordering = (
        'id',
        'name',
    )
    readonly_fields = [
    ]


admin.site.unregister(AuthGroup)
