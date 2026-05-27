from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-$-6%(p6_x)@2sc7sg6815e@fm$i%217^772(ko)wczr_@^w8r="  # noqa: S105

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nested_admin",
    "pwa",
    "courses",
    "users",
    "purchases",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.ThemeCookieMiddleware",
]

ROOT_URLCONF = "toolspaedeia.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.theme_preferences",
                "purchases.context_processors.stripe_keys",
            ],
        },
    },
]

WSGI_APPLICATION = "toolspaedeia.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files
STATICFILES_DIRS = [str(BASE_DIR / "static")]

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "users:login"

# Clickjacking protection settings
X_FRAME_OPTIONS = "SAMEORIGIN"

# PWA settings
PWA_APP_NAME = "Toolspaedeia"
PWA_APP_SHORT_NAME = "Toolspaedeia"
PWA_APP_DESCRIPTION = "A collection of tools and courses."
PWA_SERVICE_WORKER_PATH = BASE_DIR / "static" / "serviceworker.js"
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_DISPLAY = "standalone"
PWA_APP_ICONS = [
    {"src": STATIC_URL + "logo@0.5x.png", "sizes": "192x192", "type": "image/png"},
    {"src": STATIC_URL + "logo@1x.png", "sizes": "384x384", "type": "image/png"},
    {"src": STATIC_URL + "logo@2x.png", "sizes": "768x768", "type": "image/png"},
    {"src": STATIC_URL + "logo@4x.png", "sizes": "1536x1536", "type": "image/png"},
]

STRIPE_SECRET_KEY = ""
STRIPE_PUBLISHABLE_KEY = ""
STRIPE_WEBHOOK_SECRET = ""
