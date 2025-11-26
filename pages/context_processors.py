# pages/context_processors.py
from .models import SiteSettings, Announcement


def site_settings(request):
  """
  Adds `site_settings` and `announcement` to every template context.
  """
  settings_obj = SiteSettings.get_solo()
  announcement = (
      Announcement.objects.filter(is_active=True).order_by("-updated").first()
  )
  return {
      "site_settings": settings_obj,
      "announcement": announcement,
  }