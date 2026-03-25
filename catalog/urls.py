# ──────────────────────────────────────────────────────────────────────────────
# catalog/urls.py (public list/detail routes)
# ──────────────────────────────────────────────────────────────────────────────
from django.urls import path
from .views.community import CommunityListView, CommunityDetailView, CommunityShareView
from .views.plan import PlanListView, PlanDetailView, PlanShareView
from .views.home import HomeListView, HomeDetailView, HomeShareView

app_name = "catalog"
urlpatterns = [
    path("communities/", CommunityListView.as_view(), name="community_list"),
    path("communities/<slug:slug>/share/<uuid:token>/", CommunityShareView.as_view(), name="community_share"),
    path("communities/<slug:slug>/", CommunityDetailView.as_view(), name="community_detail"),
    path("plans/", PlanListView.as_view(), name="plan_list"),
    path("plans/<slug:slug>/share/<uuid:token>/", PlanShareView.as_view(), name="plan_share"),
    path("plans/<slug:slug>/", PlanDetailView.as_view(), name="plan_detail"),
    path("homes/", HomeListView.as_view(), name="home_list"),
    path("homes/<slug:slug>/share/<uuid:token>/", HomeShareView.as_view(), name="home_share"),
    path("homes/<slug:slug>/", HomeDetailView.as_view(), name="home_detail"),
]
