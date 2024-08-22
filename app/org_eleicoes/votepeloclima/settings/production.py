from .base import *

DEBUG = False

ADMINS = env.list("ADMINS", default=[("Admin", "admin@localhost")])

INSTALLED_APPS += [
    "storages",
]

# Storages

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="votepeloclima")

AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default=None)

AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")

#
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

PUBLIC_STATIC_LOCATION = "static"

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_STATIC_LOCATION}/"

STATICFILES_STORAGE = 'project.storages.PublicStaticStorage'

COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_URL = STATIC_URL

COMPRESS_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_STATIC_LOCATION}/"

PUBLIC_MEDIA_LOCATION = "media"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

DEFAULT_FILE_STORAGE = "project.storages.PublicMediaStorage"
