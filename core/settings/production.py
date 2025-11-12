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

USE_S3 = os.getenv("USE_S3", "False").lower() == "true"
if USE_S3:
    INSTALLED_APPS.append("storages")
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_QUERYSTRING_AUTH = False
else:
    # Fallback to local disk if not using S3
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"