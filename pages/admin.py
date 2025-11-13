# pages/admin.py
from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_phone", "primary_email", "updated")

    def has_add_permission(self, request):
        # Only allow one instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
