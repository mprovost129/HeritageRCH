from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser
from .models import ClientFile
@admin.register(ClientFile)
class ClientFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'client', 'uploaded_by', 'uploaded_at', 'description')
    search_fields = ('file', 'client__email', 'description')
    list_filter = ('uploaded_at',)
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'role', 'company_role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'company_role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'picture', 'phone_number_1', 'phone_number_2',
                'address_1', 'address_2', 'city', 'state', 'zip_code',
                'role', 'company_role', 'bio',
            )
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'picture', 'phone_number_1', 'phone_number_2',
                'address_1', 'address_2', 'city', 'state', 'zip_code',
                'role', 'company_role', 'bio', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('date_joined',)
