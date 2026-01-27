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


from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("employee-portal/login/", auth_views.LoginView.as_view(template_name="employee_portal/login.html"), name="employee_portal_login"),
    path("employee-portal/logout/", auth_views.LogoutView.as_view(next_page="employee_portal:dashboard"), name="employee_portal_logout"),
    path("employee-portal/password-reset/", auth_views.PasswordResetView.as_view(template_name="employee_portal/password_reset_form.html"), name="employee_portal_password_reset"),
    path("employee-portal/password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="employee_portal/password_reset_done.html"), name="employee_portal_password_reset_done"),
    path("employee-portal/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="employee_portal/password_reset_confirm.html"), name="employee_portal_password_reset_confirm"),
    path("employee-portal/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="employee_portal/password_reset_complete.html"), name="employee_portal_password_reset_complete"),
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