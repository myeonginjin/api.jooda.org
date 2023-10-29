import pymysql, boto3
from pathlib import Path

import os

SECRET_KEY = "django-insecure-x54yl6dj23y-t3-h05^bq77t*4w9273=y7jp1ev0#*ompqbr%l"
SLACK_TOKEN = "xoxb-4982936602135-5000150636772-whKm8X5LoIeN97V3nDTal2ER"
NAVER_API_CLIENT_ID = "oingm1h0rz"
NAVER_API_CLIENT_SECRET = "Iljylcie23BNUM8r9y8WcweI78O6OX2fNYsTjZJt"
HASH_SALT = "f6@@ahVnik31@!#1mkk;"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "https://jooda.org",
    "https://www.jooda.org",
    "https://api.jooda.org",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.5:3000",
]
CORS_ALLOW_CREDENTIALS = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    ###########################
    # third party
    ###########################
    # CORS
    "corsheaders",
    # Django Rest Framework
    "rest_framework",
    # Django Storages
    "storages",
    ###########################
    # App
    ###########################
    "apps.accounts",
    "apps.churchs",
    "apps.administrators",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "common.response.unexpected_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

ROOT_URLCONF = "jooda.urls"
# SET static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format1": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "format2": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "format1",
        }
    },
    # "root": {
    #     "handlers": ["console"],
    #     "level": "WARNING",
    # },
    "loggers": {
        "api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# SET Locale
LANGUAGE_CODE = "ko"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# SET Data Size in Network Communication
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000
DATA_UPLOAD_MAX_MEMORY_SIZE = 12621440
FILE_UPLOAD_MAX_MEMORY_SIZE = 12621440
