from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from pages.forms import LeadForm
from pages.models import SiteSettings
from catalog.models import Lead, LeadSource, Community, FloorPlan, AvailableHome


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        comm_qs = Community.objects.filter(is_featured=True).order_by(
            "featured_rank", "name"
        )[:3]
        plan_qs = FloorPlan.objects.filter(is_featured=True).order_by(
            "featured_rank", "name"
        )[:3]
        home_qs = (
            AvailableHome.objects.select_related("community")
            .filter(is_featured=True)
            .order_by("featured_rank", "-created")[:3]
        )

        if not comm_qs.exists():
            comm_qs = Community.objects.all()[:3]
        if not plan_qs.exists():
            plan_qs = FloorPlan.objects.all()[:3]
        if not home_qs.exists():
            home_qs = AvailableHome.objects.select_related("community")[:3]

        ctx["featured_communities"] = comm_qs
        ctx["featured_plans"] = plan_qs
        ctx["featured_homes"] = home_qs
        return ctx


class AboutView(TemplateView):
    """
    'Our Story' page.
    """
    template_name = "pages/about.html"


class CustomHomesView(TemplateView):
    template_name = "pages/custom_homes.html"


class ModelHomesView(TemplateView):
    """
    Listing / explanation page for model homes.
    """
    template_name = "pages/model_homes.html"


class TeamView(TemplateView):
    """
    'Meet Our Team' page.
    """
    template_name = "pages/team.html"


class WeBuyLandView(TemplateView):
    """
    Land acquisition / 'We Buy Land' page.
    """
    template_name = "pages/we_buy_land.html"


class MediaGalleryView(TemplateView):
    """
    Portfolio - Media Gallery.
    """
    template_name = "pages/gallery.html"


class CompletedProjectsView(TemplateView):
    """
    Portfolio - Completed Projects.
    """
    template_name = "pages/completed_projects.html"


class UpcomingProjectsView(TemplateView):
    """
    Portfolio - Upcoming / Future Projects.
    """
    template_name = "pages/upcoming_projects.html"


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = LeadForm
    success_url = reverse_lazy("pages:contact")

    def get_initial(self):
        initial = super().get_initial()
        msg = self.request.GET.get("message")
        if msg:
            initial["message"] = msg
        return initial

    def form_valid(self, form):
        # Save lead in DB
        lead = Lead.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            message=form.cleaned_data.get("message", ""),
            source=LeadSource.GLOBAL,
            page_url=self.request.build_absolute_uri(),
        )

        # Get recipients from SiteSettings.lead_recipients
        recipients = []
        try:
            settings_obj = SiteSettings.get_solo()
        except Exception:
            settings_obj = None

        if settings_obj and settings_obj.lead_recipients:
            raw = settings_obj.lead_recipients.replace(";", ",")
            for part in raw.replace("\r", "").split(","):
                email = part.strip()
                if email:
                    recipients.append(email)

        if recipients:
            body = (
                f"From: {lead.name}\n"
                f"Email: {lead.email}\n"
                f"Phone: {lead.phone}\n\n"
                f"{lead.message}"
            )
            try:
                send_mail(
                    subject=f"New website lead: {lead.name}",
                    message=body,
                    from_email=getattr(
                        settings, "DEFAULT_FROM_EMAIL", "web@localhost"
                    ),
                    recipient_list=recipients,
                    fail_silently=True,
                )
            except Exception:
                # Don’t break the user experience if email fails.
                pass

        messages.success(self.request, "Thanks! We'll be in touch shortly.")
        return super().form_valid(form)
