"""
Common settings for the Open edX
"""

from site_config_client import Client
from site_config_client.django_cache import DjangoCache
from site_config_client.google_cloud_storage import GoogleCloudStorage


def plugin_settings(settings):
    read_only_storage = GoogleCloudStorage(
        settings.SITE_CONFIG_READ_ONLY_BUCKET)
    cache = DjangoCache(
        cache_name=getattr(settings, 'SITE_CONFIG_CACHE_NAME', 'default'),
        cache_timeout=getattr(settings, 'SITE_CONFIG_CACHE_TIMEOUT', None),
    )
    settings.SITE_CONFIG_CLIENT = Client(
        base_url=settings.SITE_CONFIG_BASE_URL,
        api_token=settings.SITE_CONFIG_API_TOKEN,
        read_only_storage=read_only_storage,
        cache=cache,
    )
