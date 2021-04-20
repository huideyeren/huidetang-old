import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "qki)e^^_$phndrtm)nm^3pka!_4$53de0i)_j-gzahx(9$hwf("

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "postgres",
        "PORT": 5432,
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    "debug_toolbar",
]

MIDDLEWARE = MIDDLEWARE + [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

if "AWS_STORAGE_BUCKET_NAME" in os.environ:
    # Add django-storages to the installed apps
    INSTALLED_APPS = INSTALLED_APPS + [
        "storages",
        # "wagtail_storages",
    ]

    # https://docs.djangoproject.com/en/stable/ref/settings/#default-file-storage
    DEFAULT_FILE_STORAGE = "huidetang.aws.utils.MediaRootS3BotoStorage"

    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]

    # Disables signing of the S3 objects' URLs. When set to True it
    # will append authorization querystring to each URL.
    AWS_QUERYSTRING_AUTH = False

    # Do not allow overriding files on S3 as per Wagtail docs recommendation:
    # https://docs.wagtail.io/en/stable/advanced_topics/deploying.html#cloud-storage
    # Not having this setting may have consequences such as losing files.
    AWS_S3_FILE_OVERWRITE = False

    # Default ACL for new files should be "private" - not accessible to the
    # public. Images should be made available to public via the bucket policy,
    # where the documents should use wagtail-storages.
    AWS_DEFAULT_ACL = "public-read"

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",  # キャッシュの有効期限（最長期間）= 1日
    }

    # We generally use this setting in production to put the S3 bucket
    # behind a CDN using a custom domain, e.g. media.llamasavers.com.
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
    if "AWS_S3_CUSTOM_DOMAIN" in os.environ:
        AWS_S3_CUSTOM_DOMAIN = os.environ["AWS_S3_CUSTOM_DOMAIN"]

    # When signing URLs is enabled, the region must be set.
    # The global S3 endpoint does not seem to support signed URLS.
    # Set this only if you will be using signed URLs.
    if "AWS_S3_REGION_NAME" in os.environ:
        AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]

    # This settings lets you force using http or https protocol when generating
    # the URLs to the files. Set https as default.
    # https://github.com/jschneier/django-storages/blob/10d1929de5e0318dbd63d715db4bebc9a42257b5/storages/backends/s3boto3.py#L217
    AWS_S3_URL_PROTOCOL = os.environ.get("AWS_S3_URL_PROTOCOL", "https:")

    AWS_S3_ENDPOINT_URL = os.environ["AWS_S3_ENDPOINT_URL"]

    AWS_LOCATION = AWS_STORAGE_BUCKET_NAME

    if AWS_S3_URL_PROTOCOL == "https:":
        AWS_S3_USE_SSL = True
        AWS_S3_SECURE_URLS = True
    else:
        AWS_S3_USE_SSL = False
        AWS_S3_SECURE_URLS = False

    AWS_S3_URL = "%s" % AWS_S3_CUSTOM_DOMAIN

    STATICFILES_STORAGE = "huidetang.aws.utils.StaticRootS3BotoStorage"
    STATIC_URL = "%s//%s/%s/" % (
        AWS_S3_URL_PROTOCOL,
        AWS_S3_URL,
        "static",
    )
    MEDIA_URL = "%s//%s/%s/" % (
        AWS_S3_URL_PROTOCOL,
        AWS_S3_URL,
        "media",
    )

try:
    from .local import *
except ImportError:
    pass
