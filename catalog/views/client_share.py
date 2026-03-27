from django.http import Http404
from django.views.generic import DetailView

from ..models import CombinedClientSharePage


class CombinedClientShareView(DetailView):
    model = CombinedClientSharePage
    template_name = "catalog/combined_share.html"
    slug_field = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        token = str(self.kwargs.get("token", ""))
        if not obj.share_enabled or str(obj.share_token) != token:
            raise Http404("Share link not available.")
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.object
        section_map = {
            "home": {
                "key": "home",
                "title": "Available Home",
                "object": page.home,
            },
            "plan": {
                "key": "plan",
                "title": "Floor Plan",
                "object": page.plan,
            },
            "community": {
                "key": "community",
                "title": "Community",
                "object": page.community,
            },
        }
        ctx["ordered_sections"] = [section_map[key] for key in page.ordered_section_keys if key in section_map]
        return ctx
