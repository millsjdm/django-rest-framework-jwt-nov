# Third-Party

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup


# Local
from .forms import UserChangeForm

from .models import User


admin.site.site_header = 'Admin Backend'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)

    form = UserChangeForm
    list_display = [
        'username',
        'name',
        'email',
    ]
    list_filter = [
        'is_active',
        'is_staff',
    ]
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'username',
                'name',
                'first_name',
                'last_name',
                'email',
                'email_verified',
                'image',
                'app_metadata',
                'user_metadata',
                'roles',
                'created',
                'modified',
            )
        }),
    )
    search_fields = [
        'username',
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
        'name',
        'first_name',
        'last_name',
        'email',
        'email_verified',
        'image',
        'app_metadata',
        'user_metadata',
        'roles',
        'created',
        'modified',
    ]

admin.site.unregister(AuthGroup)
