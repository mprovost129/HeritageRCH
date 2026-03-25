# -----------------------------------------------------------------------------
# catalog/views/community.py  (for reference)
# -----------------------------------------------------------------------------
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import Http404
from ..models import Community, CommunityStatus

class CommunityListView(ListView):
    model = Community
    template_name = "catalog/community_list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().select_related()
        status = self.request.GET.get("status")
        city = self.request.GET.get("city")
        q = self.request.GET.get("q")
        if status in dict(CommunityStatus.choices):
            qs = qs.filter(status=status)
        if city:
            qs = qs.filter(city__icontains=city)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = CommunityStatus.choices
        return ctx

class CommunityDetailView(DetailView):
    model = Community
    template_name = "catalog/community_detail.html"
    slug_field = "slug"


class CommunityShareView(DetailView):
    model = Community
    template_name = "catalog/community_share.html"
    slug_field = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        token = str(self.kwargs.get("token", ""))
        if not obj.share_enabled or str(obj.share_token) != token:
            raise Http404("Share link not available.")
        return obj
