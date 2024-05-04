from config.env import env
from config.django.base import SERVER_ENV

FILE_MAX_SIZE = env.int("FILE_MAX_SIZE", default=10485760)  # 10 MiB

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_ACCESS_KEY_ID = env("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = env("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME")

if SERVER_ENV == "config.django.local":
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_URL = env("AWS_S3_URL")

elif SERVER_ENV == "config.django.dev":
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_URL = env("AWS_S3_URL")

elif SERVER_ENV == "config.django.prod":
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_URL = env("AWS_S3_URL")
