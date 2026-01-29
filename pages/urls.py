
from django.urls import path
from django.views.generic import TemplateView

from .views import (
    HomeView,
    AboutView,
    CustomHomesView,
    ModelHomesView,
    TeamView,
    WeBuyLandView,
    MediaGalleryView,
    CompletedProjectsView,
    UpcomingProjectsView,
    ContactView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("custom-homes/", CustomHomesView.as_view(), name="custom_homes"),

    # New nav pages
    path("model-homes/", ModelHomesView.as_view(), name="model_homes"),
    path("team/", TeamView.as_view(), name="team"),
    path("we-buy-land/", WeBuyLandView.as_view(), name="we_buy_land"),
    path("gallery/", MediaGalleryView.as_view(), name="gallery"),
    path("completed-projects/", CompletedProjectsView.as_view(), name="completed_projects"),
    path("upcoming-projects/", UpcomingProjectsView.as_view(), name="upcoming_projects"),

    path("contact/", ContactView.as_view(), name="contact"),
    path("our-partners/", TemplateView.as_view(template_name="pages/our_partners.html"), name="our_partners"),
]
