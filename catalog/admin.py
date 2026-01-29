from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Community,
    AvailableHome,
    Amenity,
    Photo,
    Lead,
)


# ---------------------------------------------------------------------------
# Generic inline for photos
# ---------------------------------------------------------------------------

class PhotoInline(GenericTabularInline):
    model = Photo
    extra = 1
    fields = ("image", "caption")
    verbose_name = "Photo"
    verbose_name_plural = "Photos"


# ---------------------------------------------------------------------------
# Reusable mixin for featured fields
# ---------------------------------------------------------------------------

class FeaturedAdminMixin:
    """
    Adds list_editable is_featured/featured_rank and actions to toggle featured.
    NOTE: list_display must include is_featured and featured_rank in the subclass.
    """

    list_editable = ("is_featured", "featured_rank")
    list_per_page = 25

    @admin.action(description="Mark selected as featured")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Remove from featured")
    def clear_featured(self, request, queryset):
        queryset.update(is_featured=False, featured_rank=0)

    actions = ("make_featured", "clear_featured")


# ---------------------------------------------------------------------------
# Community admin
# ---------------------------------------------------------------------------

@admin.register(Community)
class CommunityAdmin(FeaturedAdminMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "state",
        "status",
        "is_featured",
        "featured_rank",
    )
    list_filter = ("status", "city", "state", "is_featured")
    search_fields = ("name", "city", "state")
    # Only keep prepopulated_fields if Community actually has a slug field.
    # If not, you can safely remove this line.
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("featured_rank", "name")
    inlines = [PhotoInline]





# ---------------------------------------------------------------------------
# AvailableHome admin
# ---------------------------------------------------------------------------

@admin.register(AvailableHome)
class AvailableHomeAdmin(FeaturedAdminMixin, admin.ModelAdmin):
    list_display = (
        "full_address",
        "community",
        "plan",
        "status",
        "price",
        "beds",
        "baths",
        "sq_ft",
        "is_featured",
        "featured_rank",
    )
    list_filter = ("status", "community", "beds", "baths", "is_featured")
    search_fields = ("full_address", "community__name", "plan__name")
    autocomplete_fields = ("community", "plan")
    ordering = ("featured_rank", "-created")
    inlines = [PhotoInline]


# ---------------------------------------------------------------------------
# Amenity admin (simple)
# ---------------------------------------------------------------------------

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    # Removed prepopulated_fields because Amenity does not have a 'slug' field.


# ---------------------------------------------------------------------------
# Lead admin (read-only, used for following up website leads)
# ---------------------------------------------------------------------------

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "name",
        "email",
        "phone",
        "source",
        "page_url",
    )
    list_filter = ("source", "created")
    search_fields = ("name", "email", "phone", "message", "page_url")
    readonly_fields = ("created", "page_url", "source")

    fieldsets = (
        (None, {"fields": ("name", "email", "phone", "message")}),
        ("Meta", {"fields": ("source", "page_url", "created")}),
    )

    def has_add_permission(self, request):
        # Leads are created by the website, not manually
        return False
