# ──────────────────────────────────────────────────────────────────────────────
# core/settings/local.py  (developer machine)
# ──────────────────────────────────────────────────────────────────────────────
from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use SQLite locally (simple, zero-config)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email to console in dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"