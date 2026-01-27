from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from pages.models import SiteSettings
from django.urls import reverse_lazy
from catalog.models import Community, FloorPlan, AvailableHome
from .forms import CommunityForm, FloorPlanForm, AvailableHomeForm
from django.views.generic import (
    TemplateView, UpdateView, ListView, CreateView, DeleteView
)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "employee_portal/dashboard.html"

class SiteSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = SiteSettings
    fields = [
        "site_name", "primary_phone", "primary_phone_link", "primary_email",
        "address_line1", "address_line2", "city", "state", "postal_code",
        "hero_background", "hero_headline", "hero_subheadline",
        "cta_heading", "cta_body", "cta_phone_label",
        "communities_intro", "plans_intro", "homes_intro",
        "facebook_url", "instagram_url", "twitter_url", "linkedin_url", "tiktok_url"
    ]
    template_name = "employee_portal/site_settings_form.html"
    success_url = reverse_lazy("employee_portal:site_settings")

    def get_object(self):
        return SiteSettings.get_solo()

# Community CRUD
class CommunityListView(LoginRequiredMixin, ListView):
    model = Community
    template_name = "employee_portal/community_list.html"
    context_object_name = "communities"

class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    form_class = CommunityForm
    template_name = "employee_portal/community_form.html"
    success_url = reverse_lazy("employee_portal:community_list")

class CommunityUpdateView(LoginRequiredMixin, UpdateView):
    model = Community
    form_class = CommunityForm
    template_name = "employee_portal/community_form.html"
    success_url = reverse_lazy("employee_portal:community_list")

class CommunityDeleteView(LoginRequiredMixin, DeleteView):
    model = Community
    template_name = "employee_portal/community_confirm_delete.html"
    success_url = reverse_lazy("employee_portal:community_list")

# FloorPlan CRUD
class FloorPlanListView(LoginRequiredMixin, ListView):
    model = FloorPlan
    template_name = "employee_portal/plan_list.html"
    context_object_name = "plans"

class FloorPlanCreateView(LoginRequiredMixin, CreateView):
    model = FloorPlan
    form_class = FloorPlanForm
    template_name = "employee_portal/plan_form.html"
    success_url = reverse_lazy("employee_portal:plan_list")

class FloorPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = FloorPlan
    form_class = FloorPlanForm
    template_name = "employee_portal/plan_form.html"
    success_url = reverse_lazy("employee_portal:plan_list")

class FloorPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = FloorPlan
    template_name = "employee_portal/plan_confirm_delete.html"
    success_url = reverse_lazy("employee_portal:plan_list")

# AvailableHome CRUD
class AvailableHomeListView(LoginRequiredMixin, ListView):
    model = AvailableHome
    template_name = "employee_portal/home_list.html"
    context_object_name = "homes"

class AvailableHomeCreateView(LoginRequiredMixin, CreateView):
    model = AvailableHome
    form_class = AvailableHomeForm
    template_name = "employee_portal/home_form.html"
    success_url = reverse_lazy("employee_portal:home_list")

class AvailableHomeUpdateView(LoginRequiredMixin, UpdateView):
    model = AvailableHome
    form_class = AvailableHomeForm
    template_name = "employee_portal/home_form.html"
    success_url = reverse_lazy("employee_portal:home_list")

class AvailableHomeDeleteView(LoginRequiredMixin, DeleteView):
    model = AvailableHome
    template_name = "employee_portal/home_confirm_delete.html"
    success_url = reverse_lazy("employee_portal:home_list")
