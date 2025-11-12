# -----------------------------------------------------------------------------
# catalog/views/plan.py  (for reference)
# -----------------------------------------------------------------------------
from django.views.generic import ListView, DetailView
from django.db.models import Q
from ..models import FloorPlan

class PlanListView(ListView):
    model = FloorPlan
    template_name = "catalog/plan_list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        beds = self.request.GET.get("beds")
        min_sqft = self.request.GET.get("min_sqft")
        max_sqft = self.request.GET.get("max_sqft")
        q = self.request.GET.get("q")
        if beds and beds.isdigit():
            qs = qs.filter(beds__gte=int(beds))
        if min_sqft and min_sqft.isdigit():
            qs = qs.filter(sq_ft_min__gte=int(min_sqft))
        if max_sqft and max_sqft.isdigit():
            qs = qs.filter(sq_ft_max__lte=int(max_sqft))
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

class PlanDetailView(DetailView):
    model = FloorPlan
    template_name = "catalog/plan_detail.html"
    slug_field = "slug"