from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Named URL patterns for static pages
        return ["pages:home", "pages:about", "pages:custom_homes", "pages:contact"]

    def location(self, item): # type: ignore
        return reverse(item)
