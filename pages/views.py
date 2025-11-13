# -----------------------------------------------------------------------------
# pages/views.py  (FULL FILE — HomeView prefers featured, with fallback)
# -----------------------------------------------------------------------------
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from pages.forms import LeadForm
from catalog.models import Lead, LeadSource, Community, FloorPlan, AvailableHome

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        comm_qs = Community.objects.filter(is_featured=True).order_by("featured_rank", "name")[:3]
        plan_qs = FloorPlan.objects.filter(is_featured=True).order_by("featured_rank", "name")[:3]
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
        lead = Lead.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            message=form.cleaned_data.get("message", ""),
            source=LeadSource.GLOBAL,
            page_url=self.request.build_absolute_uri(),
        )
        try:
            to_addr = getattr(settings, "CONTACT_NOTIFY_EMAIL", "")
            if to_addr:
                body = (
                    f"From: {lead.name}"
                    f"Email: {lead.email}"
                    f"Phone: {lead.phone}"
                    f"{lead.message}"
                )
                send_mail(
                    subject=f"New website lead: {lead.name}",
                    message=body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "web@localhost"),
                    recipient_list=[to_addr],
                    fail_silently=True,
                )
        except Exception:
            pass
        messages.success(self.request, "Thanks! We'll be in touch shortly.")
        return super().form_valid(form)