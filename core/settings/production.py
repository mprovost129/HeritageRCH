# ──────────────────────────────────────────────────────────────────────────────
# core/settings/production.py  (for Render/Railway/Heroku)
# ──────────────────────────────────────────────────────────────────────────────
from .base import *  # noqa
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, ssl_require=False),
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    *(os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("CSRF_TRUSTED_ORIGINS") else []),
]

# Static assets (WhiteNoise pattern)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"