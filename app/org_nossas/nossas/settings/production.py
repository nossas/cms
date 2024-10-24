from .base import *

import ast

ADMINS = env("ADMINS", default="('Admin', 'admin@localhost'),")

ADMINS = ast.literal_eval(f"[{ADMINS}]")

SERVER_EMAIL = env("SERVER_EMAIL", default="no-reply@nossas.org")

MIDDLEWARE = (
    ["django_prometheus.middleware.PrometheusBeforeMiddleware"]
    + MIDDLEWARE
    + ["django_prometheus.middleware.PrometheusAfterMiddleware"]
)


INSTALLED_APPS += ["storages", "django_prometheus"]

# aws settings
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

# AWS_DEFAULT_ACL = 'public-read'

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# s3 static settings
# STATIC_LOCATION = 'static'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

# STATICFILES_STORAGE = 'project.storages.StaticStorage'

# s3 public media settings
PUBLIC_MEDIA_LOCATION = "media"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

DEFAULT_FILE_STORAGE = "project.storages.PublicMediaStorage"

if not DEBUG:

    PUBLIC_STATIC_LOCATION = "static"

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_STATIC_LOCATION}/"

    STATICFILES_STORAGE = 'project.storages.PublicStaticStorage'

    COMPRESS_STORAGE = STATICFILES_STORAGE

    COMPRESS_URL = STATIC_URL


# Configurações de e-mail
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Suporte <suporte@bonde.org>")

EMAIL_HOST = env("SMTP_HOST", default="localhost")

EMAIL_PORT = env("SMTP_PORT", default=1025)

EMAIL_HOST_USER = env("SMTP_USER", default="")

EMAIL_HOST_PASSWORD = env("SMTP_PASS", default="")

EMAIL_USE_TLS = env("SMTP_USE_TLS", default=False)

EMAIL_USE_SSL = env("SMTP_USE_SSL", default=False)