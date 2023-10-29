from .base import *

DEBUG = False
TEST = False
WSGI_APPLICATION = "jooda.wsgi.prod.application"

CSRF_TRUSTED_ORIGINS = ["https://api.jooda.org"]

### ENV ###
AWS_ACCESS_KEY_ID = "AKIARI2ND3XDBV2SQWMM"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "jooda"
DATABASES_DEFAULT_NAME = "jooda"
DATABASES_DEFAULT_USER = "admin"
DATABASES_DEFAULT_HOST = "jooda.cluster-crbvcnfpnj2t.ap-northeast-2.rds.amazonaws.com"
DATABASES_DEFAULT_PASSWORD = "BSE31S1a74bbk17xVZsw"
CACHES_DEFAULT_HOST = "redis://jooda-api-redis.jooda:6379"
JOODA_GUEST_AUTHORIZATION = "550j88000-i9n8n-41d4h-a7167-14365d44558prod"

pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASES_DEFAULT_NAME,
        "USER": DATABASES_DEFAULT_USER,
        "PASSWORD": DATABASES_DEFAULT_PASSWORD,
        "HOST": DATABASES_DEFAULT_HOST,
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHES_DEFAULT_HOST,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


# AWS setting
AWS_QUERYSTRING_AUTH = False
# S3 Storages
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (
    AWS_STORAGE_BUCKET_NAME,
    AWS_REGION,
)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
