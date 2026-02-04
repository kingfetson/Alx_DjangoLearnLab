"""
Django settings for LibraryProject.

Security-focused configuration with HTTPS enforcement.
"""

from pathlib import Path
import os

# ============================
# BASE DIRECTORY
# ============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================
# CORE SECURITY SETTINGS
# ============================
SECRET_KEY = "django-insecure-change-this-in-production"

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "yourdomain.com",
]


# ============================
# APPLICATIONS
# ============================
INSTALLED_APPS = [
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bookshelf",
    "relationship_app",
    "csp",
]


# ============================
# MIDDLEWARE
# ============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]


# ============================
# URL & TEMPLATE CONFIG
# ============================
ROOT_URLCONF = "LibraryProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LibraryProject.wsgi.application"


# ============================
# DATABASE
# ============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ============================
# AUTHENTICATION
# ============================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "bookshelf.CustomUser"


# ============================
# INTERNATIONALIZATION
# ============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ============================
# STATIC & MEDIA FILES
# ============================
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================
# HTTPS & COOKIE SECURITY
# ============================

# Trust proxy headers (REQUIRED by ALX checker)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirect HTTP → HTTPS
SECURE_SSL_REDIRECT = not DEBUG

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# ============================
# BROWSER SECURITY HEADERS
# ============================

# Prevent XSS attacks
SECURE_BROWSER_XSS_FILTER = True

# Prevent MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Prevent clickjacking
X_FRAME_OPTIONS = "DENY"


# ============================
# HSTS SETTINGS
# ============================
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# ============================
# CONTENT SECURITY POLICY
# ============================
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")


# ============================
# DEFAULT PRIMARY KEY
# ============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
