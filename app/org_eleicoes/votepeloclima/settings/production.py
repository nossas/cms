from .base import *

INSTALLED_APPS += [
    "storages",
]

# Storages

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default='votepeloclima')

AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default=None)

AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

# Compress
# 71e433d07edd

# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

PUBLIC_MEDIA_LOCATION = "media"

MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{PUBLIC_MEDIA_LOCATION}/"

# DEFAULT_FILE_STORAGE = "project.storages.PublicMediaStorage"

# COMPRESS_OFFLINE = True

# LIBSASS_OUTPUT_STYLE = 'compressed'

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# COMPRESS_ROOT = STATIC_ROOT