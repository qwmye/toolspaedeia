"""
Production settings for PythonAnywhere deployment.

Usage:
    export DJANGO_SETTINGS_MODULE=toolspaedeia.settings_production
"""

import os

from toolspaedeia.settings import *  # noqa: F403

DEBUG = False

# --- Security -----------------------------------------------------------
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

ALLOWED_HOSTS = [
    "qwmyee.pythonanywhere.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://qwmyee.pythonanywhere.com",
]

# --- Database ------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# --- HTTPS / cookie hardening -------------------------------------------
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# PWA settings
PWA_APP_DEBUG_MODE = False
