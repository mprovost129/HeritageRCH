
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
    # Community photo management
    path("communities/<int:community_id>/photos/", views.CommunityPhotoListView.as_view(), name="community_photo_list"),
    path("communities/<int:community_id>/photos/add/", views.CommunityPhotoCreateView.as_view(), name="community_photo_add"),
    path("communities/<int:community_id>/photos/<int:pk>/edit/", views.CommunityPhotoUpdateView.as_view(), name="community_photo_edit"),
    path("communities/<int:community_id>/photos/<int:pk>/delete/", views.CommunityPhotoDeleteView.as_view(), name="community_photo_delete"),
    # Home photo management
    path("homes/<int:home_id>/photos/", views.HomePhotoListView.as_view(), name="home_photo_list"),
    path("homes/<int:home_id>/photos/add/", views.HomePhotoCreateView.as_view(), name="home_photo_add"),
    path("homes/<int:home_id>/photos/<int:pk>/edit/", views.HomePhotoUpdateView.as_view(), name="home_photo_edit"),
    path("homes/<int:home_id>/photos/<int:pk>/delete/", views.HomePhotoDeleteView.as_view(), name="home_photo_delete"),
    # Plan photo management
    path("plans/<int:plan_id>/photos/", views.PlanPhotoListView.as_view(), name="plan_photo_list"),
    path("plans/<int:plan_id>/photos/add/", views.PlanPhotoCreateView.as_view(), name="plan_photo_add"),
    path("plans/<int:plan_id>/photos/<int:pk>/edit/", views.PlanPhotoUpdateView.as_view(), name="plan_photo_edit"),
    path("plans/<int:plan_id>/photos/<int:pk>/delete/", views.PlanPhotoDeleteView.as_view(), name="plan_photo_delete"),
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
    # User management
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/add/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
