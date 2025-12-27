"""
Django settings for banking_system project.
Production-ready for Render deployment.
"""

from pathlib import Path
import os

# --------------------------------------------------
# BASE
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "unsafe-dev-secret-change-me"
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "banking-uvfy.onrender.com,.onrender.com,localhost,127.0.0.1"
).split(",")

# REQUIRED for Render / reverse proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_celery_beat",

    "accounts",
    "core",
    "transactions",
]

AUTH_USER_MODEL = "accounts.User"


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------
# URLS / WSGI
# --------------------------------------------------
ROOT_URLCONF = "banking_system.urls"
WSGI_APPLICATION = "banking_system.wsgi.application"


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# AUTH / LOGIN
# --------------------------------------------------
LOGIN_REDIRECT_URL = "home"


# --------------------------------------------------
# BUSINESS SETTINGS
# --------------------------------------------------
ACCOUNT_NUMBER_START_FROM = 1000000000
MINIMUM_DEPOSIT_AMOUNT = 10
MINIMUM_WITHDRAWAL_AMOUNT = 10


# --------------------------------------------------
# CELERY (Render-safe)
# --------------------------------------------------
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
