# -----------------------------------------------------------------------------
# catalog/views/home.py  (for reference)
# -----------------------------------------------------------------------------
from django.views.generic import ListView, DetailView
from django.db.models import Q
from ..models import AvailableHome, HomeStatus

class HomeListView(ListView):
    model = AvailableHome
    template_name = "catalog/home_list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().select_related("community", "plan")
        status = self.request.GET.get("status")
        beds = self.request.GET.get("beds")
        max_price = self.request.GET.get("max_price")
        city = self.request.GET.get("city")
        q = self.request.GET.get("q")
        if status in dict(HomeStatus.choices):
            qs = qs.filter(status=status)
        if beds and beds.isdigit():
            qs = qs.filter(beds__gte=int(beds))
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass
        if city:
            qs = qs.filter(city__icontains=city)
        if q:
            qs = qs.filter(Q(address_1__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = HomeStatus.choices
        return ctx

class HomeDetailView(DetailView):
    model = AvailableHome
    template_name = "catalog/home_detail.html"
    slug_field = "slug"
