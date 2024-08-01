from .base import *

INSTALLED_APPS += [
    "storages",
]

# Storages

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = 'votepeloclima'

AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default=None)

AWS_S3_REGION_NAME = env('AWS_STORAGE_BUCKET_NAME', default='us-east-1')