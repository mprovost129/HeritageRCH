# ──────────────────────────────────────────────────────────────────────────────
# core/manage.py  (replace your existing manage.py with this or copy the env line)
# ──────────────────────────────────────────────────────────────────────────────
import os
import sys


def ensure_postgres_schema():
    settings_module = os.getenv("DJANGO_SETTINGS_MODULE", "")
    database_url = os.getenv("DATABASE_URL", "")
    schema_name = os.getenv("DB_SCHEMA", "").strip()

    if settings_module != "core.settings.production":
        return
    if not schema_name:
        return
    if not database_url.startswith(("postgres://", "postgresql://")):
        return

    import psycopg
    from psycopg import sql

    with psycopg.connect(database_url, autocommit=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))


def main():
    # Default to local settings for dev if not already set
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")
    ensure_postgres_schema()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
