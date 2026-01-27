from django.urls import path
from . import views

app_name = "employee_portal"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("site-settings/", views.SiteSettingsUpdateView.as_view(), name="site_settings"),
    # Community CRUD
    path("communities/", views.CommunityListView.as_view(), name="community_list"),
    path("communities/add/", views.CommunityCreateView.as_view(), name="community_add"),
    path("communities/<int:pk>/edit/", views.CommunityUpdateView.as_view(), name="community_edit"),
    path("communities/<int:pk>/delete/", views.CommunityDeleteView.as_view(), name="community_delete"),
    # FloorPlan CRUD
    path("plans/", views.FloorPlanListView.as_view(), name="plan_list"),
    path("plans/add/", views.FloorPlanCreateView.as_view(), name="plan_add"),
    path("plans/<int:pk>/edit/", views.FloorPlanUpdateView.as_view(), name="plan_edit"),
    path("plans/<int:pk>/delete/", views.FloorPlanDeleteView.as_view(), name="plan_delete"),
    # Home CRUD
    path("homes/", views.AvailableHomeListView.as_view(), name="home_list"),
    path("homes/add/", views.AvailableHomeCreateView.as_view(), name="home_add"),
    path("homes/<int:pk>/edit/", views.AvailableHomeUpdateView.as_view(), name="home_edit"),
    path("homes/<int:pk>/delete/", views.AvailableHomeDeleteView.as_view(), name="home_delete"),
]
