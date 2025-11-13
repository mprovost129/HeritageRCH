# -----------------------------------------------------------------------------
# catalog/admin.py  (FULL FILE — list_editable toggles for featured)
# -----------------------------------------------------------------------------
from django.contrib import admin
from .models import Amenity, Community, FloorPlan, AvailableHome, Photo, Lead

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "caption", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("caption",)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "status", "is_featured", "featured_rank")
    list_filter = ("status", "city", "state", "is_featured")
    search_fields = ("name", "city", "state")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("amenities", "available_plans")
    list_editable = ("is_featured", "featured_rank")

@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "beds", "baths", "sq_ft_min", "sq_ft_max", "is_featured", "featured_rank")
    list_filter = ("beds", "is_featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_featured", "featured_rank")

@admin.register(AvailableHome)
class AvailableHomeAdmin(admin.ModelAdmin):
    list_display = ("slug", "community", "status", "price", "beds", "baths", "is_featured", "featured_rank")
    list_filter = ("status", "community", "is_featured")
    search_fields = ("slug", "address_1", "city", "postal_code")
    prepopulated_fields = {"slug": ("address_1",)}
    list_editable = ("is_featured", "featured_rank")

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "source", "created")
    list_filter = ("source", "created")
    search_fields = ("name", "email", "phone", "message")