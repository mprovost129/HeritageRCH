# ──────────────────────────────────────────────────────────────────────────────
# catalog/admin.py
# ──────────────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Amenity,
    Attachment,
    AvailableHome,
    Community,
    FloorPlan,
    GalleryItem,
    Photo,
    PlanAvailability,
    PlanSeries,
    Lead,
)


class PhotoInline(GenericTabularInline):
    model = Photo
    extra = 1
    fields = ("image", "caption", "order", "preview")
    readonly_fields = ("preview",)
    ct_field = "content_type"
    ct_fk_field = "object_id"

    def preview(self, obj):  # pragma: no cover
        if getattr(obj, "image", None):
            return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
        return "—"


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1
    fields = ("title", "file")
    ct_field = "content_type"
    ct_fk_field = "object_id"


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "status")
    list_filter = ("status", "city", "state")
    search_fields = ("name", "city", "county", "school_district")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PhotoInline, AttachmentInline]


@admin.register(PlanSeries)
class PlanSeriesAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    verbose_name_plural = "Plan Series"


class PlanAvailabilityInline(admin.TabularInline):
    model = PlanAvailability
    extra = 0


@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "series", "beds", "baths", "garage_cars", "sq_ft_min", "sq_ft_max")
    list_filter = ("series", "beds", "garage_cars")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PhotoInline, AttachmentInline, PlanAvailabilityInline]


@admin.register(AvailableHome)
class AvailableHomeAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "community",
        "status",
        "price",
        "beds",
        "baths",
        "sq_ft",
        "ready_date",
    )
    list_filter = ("community", "status", "beds")
    search_fields = ("slug", "address_1", "lot_number", "mls_number")
    prepopulated_fields = {"slug": ("community", "lot_number", "address_1")}
    inlines = [PhotoInline, AttachmentInline]


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "order")
    list_filter = ("category",)
    search_fields = ("title", "caption")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "phone", "source")
    list_filter = ("source", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at", "updated_at")
