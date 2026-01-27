# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
# App/model imports
from catalog.models import AvailableHome, FloorPlan, Photo
from employee_portal.photo_forms import PhotoForm
# Home Photo Management
class HomePhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "employee_portal/home_photo_list.html"
    context_object_name = "photos"
    def get_queryset(self):
        self.home = get_object_or_404(AvailableHome, pk=self.kwargs["home_id"])
        return Photo.objects.filter(content_type__model="availablehome", object_id=self.home.pk)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["home"] = self.home
        return ctx
class HomePhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/home_photo_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.home = get_object_or_404(AvailableHome, pk=kwargs["home_id"])
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.content_object = self.home
        photo.save()
        return redirect("employee_portal:home_photo_list", home_id=self.home.pk)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["home"] = self.home
        return ctx
class HomePhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/home_photo_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.home = get_object_or_404(AvailableHome, pk=kwargs["home_id"])
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("employee_portal:home_photo_list", kwargs={"home_id": self.home.pk})
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["home"] = self.home
        return ctx
class HomePhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = "employee_portal/home_photo_confirm_delete.html"
    def dispatch(self, request, *args, **kwargs):
        self.home = get_object_or_404(AvailableHome, pk=kwargs["home_id"])
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("employee_portal:home_photo_list", kwargs={"home_id": self.home.pk})
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["home"] = self.home
        return ctx

# Plan Photo Management
class PlanPhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "employee_portal/plan_photo_list.html"
    context_object_name = "photos"
    def get_queryset(self):
        self.plan = get_object_or_404(FloorPlan, pk=self.kwargs["plan_id"])
        return Photo.objects.filter(content_type__model="floorplan", object_id=self.plan.pk)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plan"] = self.plan
        return ctx
class PlanPhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/plan_photo_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.plan = get_object_or_404(FloorPlan, pk=kwargs["plan_id"])
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.content_object = self.plan
        photo.save()
        return redirect("employee_portal:plan_photo_list", plan_id=self.plan.pk)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plan"] = self.plan
        return ctx
class PlanPhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/plan_photo_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.plan = get_object_or_404(FloorPlan, pk=kwargs["plan_id"])
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("employee_portal:plan_photo_list", kwargs={"plan_id": self.plan.pk})
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plan"] = self.plan
        return ctx
class PlanPhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = "employee_portal/plan_photo_confirm_delete.html"
    def dispatch(self, request, *args, **kwargs):
        self.plan = get_object_or_404(FloorPlan, pk=kwargs["plan_id"])
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("employee_portal:plan_photo_list", kwargs={"plan_id": self.plan.pk})
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plan"] = self.plan
        return ctx
from catalog.models import Photo, Community
from .photo_forms import PhotoForm
from django.shortcuts import get_object_or_404, redirect
# Community Photo Management
class CommunityPhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "employee_portal/community_photo_list.html"
    context_object_name = "photos"

    def get_queryset(self):
        self.community = get_object_or_404(Community, pk=self.kwargs["community_id"])
        return Photo.objects.filter(content_type__model="community", object_id=self.community.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["community"] = self.community
        return ctx

class CommunityPhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/community_photo_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.community = get_object_or_404(Community, pk=kwargs["community_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.content_object = self.community
        photo.save()
        return redirect("employee_portal:community_photo_list", community_id=self.community.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["community"] = self.community
        return ctx

class CommunityPhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "employee_portal/community_photo_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.community = get_object_or_404(Community, pk=kwargs["community_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("employee_portal:community_photo_list", kwargs={"community_id": self.community.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["community"] = self.community
        return ctx

class CommunityPhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = "employee_portal/community_photo_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        self.community = get_object_or_404(Community, pk=kwargs["community_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("employee_portal:community_photo_list", kwargs={"community_id": self.community.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["community"] = self.community
        return ctx
from django.contrib.auth.models import User
from .user_forms import UserForm
from django.contrib.auth.mixins import UserPassesTestMixin
# User management views (superuser/staff only)
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "employee_portal/user_list.html"
    context_object_name = "users"
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "employee_portal/user_form.html"
    success_url = reverse_lazy("employee_portal:user_list")
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "employee_portal/user_form.html"
    success_url = reverse_lazy("employee_portal:user_list")
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "employee_portal/user_confirm_delete.html"
    success_url = reverse_lazy("employee_portal:user_list")
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
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
