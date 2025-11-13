# ──────────────────────────────────────────────────────────────────────────────
# pages/urls.py
# ──────────────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import HomeView, ContactView, AboutView, CustomHomesView

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("custom-homes/", CustomHomesView.as_view(), name="custom_homes"),
    path("contact/", ContactView.as_view(), name="contact"),
]