# ──────────────────────────────────────────────────────────────────────────────
# catalog/urls.py (public list/detail routes)
# ──────────────────────────────────────────────────────────────────────────────
from django.urls import path
from .views.community import CommunityListView, CommunityDetailView
from .views.plan import PlanListView, PlanDetailView
from .views.home import HomeListView, HomeDetailView

app_name = "catalog"
urlpatterns = [
    path("communities/", CommunityListView.as_view(), name="community_list"),
    path("communities/<slug:slug>/", CommunityDetailView.as_view(), name="community_detail"),
    path("plans/", PlanListView.as_view(), name="plan_list"),
    path("plans/<slug:slug>/", PlanDetailView.as_view(), name="plan_detail"),
    path("homes/", HomeListView.as_view(), name="home_list"),
    path("homes/<slug:slug>/", HomeDetailView.as_view(), name="home_detail"),
]
