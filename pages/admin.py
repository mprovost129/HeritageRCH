from django.contrib import admin

from .models import SiteSettings, Announcement


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_phone", "primary_email", "updated")
    readonly_fields = ("updated",)

    fieldsets = (
        ("Brand & Site Name", {
            "fields": ("site_name",),
        }),
        ("Contact Info", {
            "fields": (
                "primary_phone",
                "primary_phone_link",
                "primary_email",
            ),
        }),
        ("Lead Notifications", {
            "description": (
                "Emails entered here will receive website leads from the contact form. "
                "You can enter one or more addresses, separated by commas or line breaks."
            ),
            "fields": ("lead_recipients",),
        }),
        ("Office Address", {
            "fields": (
                "address_line1",
                "address_line2",
                "city",
                "state",
                "postal_code",
            ),
        }),
        ("Homepage Hero", {
            "fields": (
                "hero_background",
                "hero_headline",
                "hero_subheadline",
            ),
        }),
        ("Global CTA Strip", {
            "fields": (
                "cta_heading",
                "cta_body",
                "cta_phone_label",
            ),
        }),
        ("Page Intros", {
            "fields": (
                "communities_intro",
                "plans_intro",
                "homes_intro",
            ),
        }),
        ("System", {
            "fields": ("updated",),
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated")
    list_filter = ("is_active", "updated")
    search_fields = ("title", "message")
    list_editable = ("is_active",)
    ordering = ("-updated",)
