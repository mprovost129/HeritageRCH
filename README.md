# ──────────────────────────────────────────────────────────────────────────────
# README (deploy quick start)
# ──────────────────────────────────────────────────────────────────────────────
# 1) Push repo to GitHub.
# 2) In Render, "New +" → Web Service → connect repo → Python.
#    Build:  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
#    Start:  gunicorn core.wsgi --log-file - --workers=3 --timeout=120
#    Environment: set DJANGO_SETTINGS_MODULE=core.settings.production, generate SECRET_KEY, add ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS.
# 3) Add a PostgreSQL database in Render; set DATABASE_URL automatically via the dashboard or render.yaml.
# 4) After first deploy, open the service → Shell → run `python manage.py createsuperuser` if needed.
# 5) Add Custom Domain in Render (e.g., www.heritagerch.com). Render will give DNS targets.
# 6) In GoDaddy DNS: create a CNAME for `www` → the Render provided target. Set apex `heritagerch.com` to forward to https://www.heritagerch.com/ (or move DNS to Cloudflare to CNAME-flatten the apex).
# 7) Verify HTTPS is active, test admin and public pages, and you’re live.