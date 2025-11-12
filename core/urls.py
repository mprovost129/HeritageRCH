# ──────────────────────────────────────────────────────────────────────────────
# core/urls.py (homepage enabled + catalog + media)
# ──────────────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("pages.urls", "pages"), namespace="pages")),  # home & contact
    path("", include(("catalog.urls", "catalog"), namespace="catalog")),  # communities, plans, homes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin branding
admin.site.site_header = "Heritage RCH Admin"
admin.site.site_title = "Heritage RCH Admin"
admin.site.index_title = "Dashboard"