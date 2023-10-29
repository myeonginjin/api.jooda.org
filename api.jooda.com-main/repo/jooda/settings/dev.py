from .base import *

DEBUG = True
TEST = False
WSGI_APPLICATION = "jooda.wsgi.dev.application"

### ENV ###
AWS_ACCESS_KEY_ID = "AKIA3LFXBK2C3E6VP6FA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "jooda-dev"
DATABASES_DEFAULT_NAME = "jooda"
DATABASES_DEFAULT_USER = "admin"
DATABASES_DEFAULT_HOST = "fooiy-dev.c8v42wdxujxn.ap-northeast-2.rds.amazonaws.com"
DATABASES_DEFAULT_PASSWORD = "fdsbhAAbj1afdaFDVZsw"
CACHES_DEFAULT_HOST = "redis://jooda-api-redis.jooda:6379"
JOODA_GUEST_AUTHORIZATION = "550n88ji0-ehoob-nna98-b7167-446655447874dev"

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
