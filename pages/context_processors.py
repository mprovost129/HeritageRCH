# pages/context_processors.py
from .models import SiteSettings, Announcement
from django.db.utils import DatabaseError


def site_settings(request):
  """
  Adds `site_settings` and `announcement` to every template context.
  """
  try:
      settings_obj = SiteSettings.get_solo()
      announcement = (
          Announcement.objects.filter(is_active=True).order_by("-updated").first()
      )
  except DatabaseError:
      settings_obj = None
      announcement = None
  return {
      "site_settings": settings_obj,
      "announcement": announcement,
  }
