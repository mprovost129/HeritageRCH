# pages/context_processors.py
from .models import SiteSettings


def site_settings(request):
    """
    Adds `site_settings` to every template context.
    """
    return {
        "site_settings": SiteSettings.get_solo(),
    }
