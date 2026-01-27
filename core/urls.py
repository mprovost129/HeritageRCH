# ──────────────────────────────────────────────────────────────────────────────
# core/urls.py (homepage enabled + catalog + media)
# ──────────────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from catalog.sitemaps import CommunitySitemap, FloorPlanSitemap, HomeSitemap
from pages.sitemaps import StaticViewSitemap

sitemaps = {
    "communities": CommunitySitemap,
    "plans": FloorPlanSitemap,
    "homes": HomeSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("employee-portal/", include(("employee_portal.urls", "employee_portal"), namespace="employee_portal")),
    path("", include(("pages.urls", "pages"), namespace="pages")),
    path("", include(("catalog.urls", "catalog"), namespace="catalog")),

    # SEO endpoints
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin branding
admin.site.site_header = "Heritage RCH Admin"
admin.site.site_title = "Heritage RCH Admin"
admin.site.index_title = "Dashboard"