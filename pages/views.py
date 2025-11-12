# ──────────────────────────────────────────────────────────────────────────────
# pages/views.py
# ──────────────────────────────────────────────────────────────────────────────
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlencode
from catalog.models import Lead, LeadSource
from pages.forms import LeadForm

class HomeView(TemplateView):
    template_name = "pages/home.html"

class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = LeadForm
    success_url = reverse_lazy("pages:contact")

    def form_valid(self, form):
        Lead.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            message=form.cleaned_data.get("message", ""),
            source=LeadSource.GLOBAL,
            page_url=self.request.build_absolute_uri(),
        )
        messages.success(self.request, "Thanks! We'll be in touch shortly.")
        return super().form_valid(form)