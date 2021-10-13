"""Common settings for the Open edX."""


from site_config_client import Client
from site_config_client.google_cloud_storage import GoogleCloudStorage
# from site_config_client.django_cache import DjangoCache


def plugin_settings(settings):
    read_only_storage = GoogleCloudStorage(settings.SITE_CONFIG_READ_ONLY_BUCKET)
    # cache = DjangoCache(timeout=settings.SITE_CONFIG_CAHCE_TIMEOUT)
    settings.SITE_CONFIG_CLIENT = Client(
        base_url=settings.SITE_CONFIG_BASE_URL,
        api_token=settings.SITE_CONFIG_API_TOKEN,
        read_only_storage=read_only_storage,
        # cache=cache,
    )


"""
TODO: Goal 2. run this on devstack/staging
# install via devstack
# https://github.com/appsembler/devstack/#persistent-custom-python-packages

# make lms-shell
# ./manage.py lms shell

>>> from django.conf import settings
>>> client = settings.SITE_CONFIG_CLIENT
>>> client.get_backend_configs('somehard-coded-uuid', 'live')
"""
