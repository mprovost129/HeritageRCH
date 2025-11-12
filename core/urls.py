# ──────────────────────────────────────────────────────────────────────────────
# core/urls.py (updated to include catalog + media in dev)
# ──────────────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Send the home page to Communities for now (quick fix for 404 at "/")
    path("", RedirectView.as_view(pattern_name="catalog:community_list", permanent=False)),

    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin branding (optional)
admin.site.site_header = "Heritage RCH Admin"
admin.site.site_title = "Heritage RCH Admin"
admin.site.index_title = "Dashboard"