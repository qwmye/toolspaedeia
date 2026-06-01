import os
from urllib.parse import parse_qsl
from urllib.parse import urlparse

from toolspaedeia.settings import *  # noqa: F403

DEBUG = False

# --- Security -----------------------------------------------------------
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

ALLOWED_HOSTS = [
    "qwmyee.pythonanywhere.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://qwmyee.pythonanywhere.com",
]

# --- Database ------------------
postgres_db_url = urlparse(os.environ["DATABASE_URL"])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": postgres_db_url.path.replace("/", ""),
        "USER": postgres_db_url.username,
        "PASSWORD": postgres_db_url.password,
        "HOST": postgres_db_url.hostname,
        "PORT": 5432,
        "OPTIONS": dict(parse_qsl(postgres_db_url.query)),
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
