# ──────────────────────────────────────────────────────────────────────────────
# core/manage.py  (replace your existing manage.py with this or copy the env line)
# ──────────────────────────────────────────────────────────────────────────────
import os
import sys

def main():
    # Default to local settings for dev if not already set
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
