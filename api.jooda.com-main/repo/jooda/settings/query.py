from .dev import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "format",
        }
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
