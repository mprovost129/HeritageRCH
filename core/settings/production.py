# ──────────────────────────────────────────────────────────────────────────────
# core/settings/production.py  (for Render/Railway/Heroku)
# ──────────────────────────────────────────────────────────────────────────────
from .base import *  # noqa
import os
from pathlib import Path
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, ssl_require=False),
}

# Isolate this site inside a dedicated PostgreSQL schema when sharing one database.
DB_SCHEMA = os.getenv("DB_SCHEMA", "heritage_rch").strip()
db_options = DATABASES["default"].setdefault("OPTIONS", {})
existing_options = db_options.get("options", "").strip()
schema_option = f"-c search_path={DB_SCHEMA},public"
if schema_option not in existing_options:
    db_options["options"] = f"{existing_options} {schema_option}".strip()

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

    # Accept common env var names used by Render/S3-compatible providers.
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("S3_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("S3_SECRET_ACCESS_KEY")
    AWS_S3_MEDIA_BUCKET = (
        os.getenv("AWS_S3_MEDIA_BUCKET")
        or os.getenv("AWS_BUCKET_NAME")
        or os.getenv("S3_BUCKET_NAME")
    )
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME") or os.getenv("AWS_REGION")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL") or os.getenv("S3_ENDPOINT_URL")
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = os.getenv("AWS_QUERYSTRING_AUTH", "false").lower() == "true"

    # Django 5+ preferred storage config.
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }

    # Optional explicit media URL when using a CDN/custom domain.
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
else:
    # Fallback to local disk if not using S3
    MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
    MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", str(BASE_DIR / "media")))
