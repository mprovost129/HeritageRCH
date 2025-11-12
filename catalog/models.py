# ──────────────────────────────────────────────────────────────────────────────
# catalog/models.py
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

from decimal import Decimal
from typing import Optional

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


# ──────────────────────────────────────────────────────────────────────────────
# Helpers / Base
# ──────────────────────────────────────────────────────────────────────────────

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    slug = models.SlugField(max_length=160, unique=True, help_text="URL slug")

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True, help_text="US state code, e.g. MA")
    postal_code = models.CharField(max_length=20, blank=True)

    class Meta:
        abstract = True

    @property
    def full_address(self) -> str:
        parts = [self.address_1, self.address_2, self.city, self.state, self.postal_code]
        return ", ".join([p for p in parts if p])


# ──────────────────────────────────────────────────────────────────────────────
# Taxonomy / Shared assets
# ──────────────────────────────────────────────────────────────────────────────

class Amenity(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Attachment(TimeStampedModel):
    """
    Generic file attachment for any object (e.g., HOA docs, spec sheets).
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="attachments/%Y/%m/%d/")

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Photo(TimeStampedModel):
    """
    Generic photo association for Communities, Plans, Homes, or Gallery items.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta: # type: ignore
        ordering = ["order", "id"]

    def __str__(self) -> str:  # pragma: no cover
        return self.caption or f"Photo #{self.pk}"


# ──────────────────────────────────────────────────────────────────────────────
# Core domain: Communities, Floor Plans, Available Homes
# ──────────────────────────────────────────────────────────────────────────────

class CommunityStatus(models.TextChoices):
    COMING_SOON = "coming", "Coming Soon"
    ACTIVE = "active", "Active"
    CLOSING_OUT = "closing", "Closing Out"
    SOLD_OUT = "sold_out", "Sold Out"


class Community(TimeStampedModel, SluggedModel):
    name = models.CharField(max_length=160)
    tagline = models.CharField(max_length=200, blank=True)

    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=CommunityStatus.choices, default=CommunityStatus.ACTIVE
    )

    # Geo
    city = models.CharField(max_length=120, blank=True)
    county = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, default="MA")
    school_district = models.CharField(max_length=160, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Amenities & media
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="communities")
    photos = GenericRelation(Photo)
    attachments = GenericRelation(Attachment)

    class Meta: # type: ignore
        ordering = ["name"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["city", "state"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return self.name

    def get_absolute_url(self):  # pragma: no cover
        return reverse("catalog:community_detail", args=[self.slug])


class PlanSeries(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class FloorPlan(TimeStampedModel, SluggedModel):
    name = models.CharField(max_length=160)
    series = models.ForeignKey(
        PlanSeries, on_delete=models.SET_NULL, null=True, blank=True, related_name="plans"
    )

    beds = models.PositiveSmallIntegerField(default=3)
    baths = models.DecimalField(
        max_digits=3, decimal_places=1, default=Decimal("2.0"), validators=[MinValueValidator(0)]
    )
    garage_cars = models.PositiveSmallIntegerField(default=2)

    sq_ft_min = models.PositiveIntegerField(null=True, blank=True)
    sq_ft_max = models.PositiveIntegerField(null=True, blank=True)

    base_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, help_text="Optional from-price"
    )

    description = models.TextField(blank=True)
    brochure_pdf = models.FileField(upload_to="plans/brochures/%Y/%m/%d/", blank=True)

    photos = GenericRelation(Photo)
    attachments = GenericRelation(Attachment)

    # Which communities this plan is available in (with per-community overrides)
    available_in = models.ManyToManyField(
        Community, through="PlanAvailability", related_name="available_plans", blank=True
    )

    class Meta: # type: ignore
        ordering = ["name"]
        indexes = [
            models.Index(fields=["beds", "baths"]),
            models.Index(fields=["sq_ft_min", "sq_ft_max"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return self.name

    def get_absolute_url(self):  # pragma: no cover
        return reverse("catalog:plan_detail", args=[self.slug])


class PlanAvailability(models.Model):
    """
    Through table for FloorPlan <-> Community with useful overrides.
    """

    plan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    is_available = models.BooleanField(default=True)
    base_price_override = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("plan", "community")
        verbose_name_plural = "Plan availability"

    def __str__(self) -> str:  # pragma: no cover
        price = self.base_price_override or self.plan.base_price
        return f"{self.plan} in {self.community} ({'Available' if self.is_available else 'Hidden'})" + (
            f" — ${price:,.0f}" if price else ""
        )


class HomeStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    UNDER_CONSTRUCTION = "uc", "Under Construction"
    PENDING = "pending", "Pending"
    SOLD = "sold", "Sold"
    COMING_SOON = "coming", "Coming Soon"


class AvailableHome(TimeStampedModel, AddressMixin, SluggedModel):
    """
    A specific inventory home/lot, optionally based on a FloorPlan.
    """

    community = models.ForeignKey(Community, on_delete=models.PROTECT, related_name="homes")
    plan = models.ForeignKey(
        FloorPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name="homes"
    )

    lot_number = models.CharField(max_length=50, blank=True)
    mls_number = models.CharField(max_length=50, blank=True)

    status = models.CharField(max_length=20, choices=HomeStatus.choices, default=HomeStatus.ACTIVE)
    ready_date = models.DateField(null=True, blank=True, help_text="Target completion/ready date")

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    beds = models.PositiveSmallIntegerField(default=3)
    baths = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("2.0"))
    garage_cars = models.PositiveSmallIntegerField(default=2)
    sq_ft = models.PositiveIntegerField(null=True, blank=True)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)

    description = models.TextField(blank=True)

    photos = GenericRelation(Photo)
    attachments = GenericRelation(Attachment)

    class Meta: # type: ignore
        ordering = ["community__name", "lot_number", "address_1"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["community", "status"]),
            models.Index(fields=["beds", "baths"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        base = self.full_address or self.lot_number or self.slug
        return f"{base} — {self.community.name}"

    def get_absolute_url(self):  # pragma: no cover
        return reverse("catalog:home_detail", args=[self.slug])


# ──────────────────────────────────────────────────────────────────────────────
# Gallery — site-wide inspiration library
# ──────────────────────────────────────────────────────────────────────────────

class GalleryCategory(models.TextChoices):
    EXTERIOR = "exterior", "Exterior"
    KITCHEN = "kitchen", "Kitchens"
    BATHROOM = "bathroom", "Bathrooms"
    FIREPLACE = "fireplace", "Fireplaces"
    STAIRS = "stairs", "Stairs"
    OTHER = "other", "Other Rooms"


class GalleryItem(TimeStampedModel):
    category = models.CharField(max_length=30, choices=GalleryCategory.choices)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="gallery/%Y/%m/%d/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    # Optional linkage back to a specific plan/home/community
    linked_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    linked_object_id = models.PositiveIntegerField(null=True, blank=True)
    linked_object = GenericForeignKey("linked_content_type", "linked_object_id")

    class Meta: # type: ignore
        ordering = ["order", "id"]

    def __str__(self) -> str:  # pragma: no cover
        return self.title or f"Gallery #{self.pk}"


# ──────────────────────────────────────────────────────────────────────────────
# Leads — captured from Plan/Home/Community/Global forms
# ──────────────────────────────────────────────────────────────────────────────

class LeadSource(models.TextChoices):
    GLOBAL = "global", "Site-wide form"
    COMMUNITY = "community", "Community page"
    PLAN = "plan", "Plan page"
    HOME = "home", "Available home page"
    OTHER = "other", "Other"


class Lead(TimeStampedModel):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)

    message = models.TextField(blank=True)
    source = models.CharField(max_length=30, choices=LeadSource.choices, default=LeadSource.GLOBAL)

    # Generic target reference (optional)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey("target_content_type", "target_object_id")

    page_url = models.URLField(blank=True, help_text="Page URL where the lead was submitted")

    class Meta: # type: ignore
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"Lead from {self.name} ({self.email})"