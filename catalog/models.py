# -----------------------------------------------------------------------------
# catalog/models.py  (FULL FILE — adds is_featured & featured_rank on 3 models)
# -----------------------------------------------------------------------------
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Amenity(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.name

class Photo(TimeStamped):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    image = models.ImageField(upload_to="photos/")
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: # type: ignore
        ordering = ("sort_order", "id")
    def __str__(self):
        return self.caption or f"Photo #{self.pk}"

class CommunityStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    COMING = "coming", "Coming Soon"
    CLOSING = "closing", "Closing Out"
    SOLD_OUT = "sold_out", "Sold Out"

class Community(TimeStamped):
    slug = models.SlugField(max_length=160, unique=True)
    name = models.CharField(max_length=160)
    tagline = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    status = models.CharField(max_length=20, choices=CommunityStatus.choices, default=CommunityStatus.ACTIVE)
    description = models.TextField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="communities")
    photos = GenericRelation(Photo, related_query_name="community")
    # FEATURE FLAGS
    is_featured = models.BooleanField(default=False, db_index=True)
    featured_rank = models.PositiveIntegerField(default=0, help_text="Lower shows first among featured")

    available_plans = models.ManyToManyField("FloorPlan", blank=True, related_name="available_in")

    class Meta: # type: ignore
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:150]
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:community_detail", args=[self.slug])

class FloorPlan(TimeStamped):
    slug = models.SlugField(max_length=160, unique=True)
    name = models.CharField(max_length=160)
    beds = models.PositiveSmallIntegerField(default=0)
    baths = models.DecimalField(max_digits=4, decimal_places=1, default=0) # type: ignore
    sq_ft_min = models.PositiveIntegerField(null=True, blank=True)
    sq_ft_max = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    photos = GenericRelation(Photo, related_query_name="plan")
    # FEATURE FLAGS
    is_featured = models.BooleanField(default=False, db_index=True)
    featured_rank = models.PositiveIntegerField(default=0)

    class Meta: # type: ignore
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:150]
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:plan_detail", args=[self.slug])

class HomeStatus(models.TextChoices):
    COMING = "coming", "Coming Soon"
    UC = "uc", "Under Construction"
    ACTIVE = "active", "Active"
    PENDING = "pending", "Pending"
    SOLD = "sold", "Sold"

class AvailableHome(TimeStamped):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="homes")
    plan = models.ForeignKey(FloorPlan, on_delete=models.SET_NULL, related_name="homes", null=True, blank=True)
    slug = models.SlugField(max_length=160, unique=True)
    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postal_code = models.CharField(max_length=12, blank=True)
    beds = models.PositiveSmallIntegerField(default=0)
    baths = models.DecimalField(max_digits=4, decimal_places=1, default=0) # type: ignore
    sq_ft = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=HomeStatus.choices, default=HomeStatus.COMING)
    description = models.TextField(blank=True)
    photos = GenericRelation(Photo, related_query_name="home")
    # FEATURE FLAGS
    is_featured = models.BooleanField(default=False, db_index=True)
    featured_rank = models.PositiveIntegerField(default=0)

    class Meta: # type: ignore
        ordering = ("-created",)

    def __str__(self):
        return self.full_address or self.slug

    @property
    def full_address(self):
        parts = [self.address_1, self.city, self.state, self.postal_code]
        if any(parts):
            city_line = " ".join(p for p in [self.city, self.state, self.postal_code] if p)
            return ", ".join([p for p in [self.address_1, city_line] if p])
        return ""

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.full_address or f"home-{self.pk or ''}"
            self.slug = slugify(base)[:150]
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:home_detail", args=[self.slug])

class LeadSource(models.TextChoices):
    GLOBAL = "site", "Website"
    PLAN = "plan", "Plan Page"
    COMMUNITY = "community", "Community Page"
    HOME = "home", "Home Page"

class Lead(TimeStamped):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=20, choices=LeadSource.choices, default=LeadSource.GLOBAL)
    page_url = models.URLField(blank=True)
    def __str__(self):
        return f"{self.name} <{self.email}>"
