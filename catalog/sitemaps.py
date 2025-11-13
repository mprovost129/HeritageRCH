from django.contrib.sitemaps import Sitemap
from .models import Community, FloorPlan, AvailableHome

class CommunitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Community.objects.all()

    def lastmod(self, obj):
        return obj.updated

class FloorPlanSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return FloorPlan.objects.all()

    def lastmod(self, obj):
        return obj.updated

class HomeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return AvailableHome.objects.all()

    def lastmod(self, obj):
        return obj.updated
